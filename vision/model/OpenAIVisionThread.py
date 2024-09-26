import time

import openai
from PyQt6.QtCore import QThread, pyqtSignal
from openai import OpenAI

from util.Constants import Constants


class OpenAIVisionThread(QThread):
    response_signal = pyqtSignal(str, bool)
    response_finished_signal = pyqtSignal(str, str, float, bool)

    def __init__(self, args):
        super().__init__()
        self.openai_arg = args['ai_arg']
        self.openai = OpenAI(api_key=args['api_key'])
        self.stream = self.openai_arg['stream']
        self.force_stop = False
        self.start_time = None

    def run(self):
        self.start_time = time.time()
        try:
            response = self.get_response(self.openai_arg)
            if isinstance(response, openai.Stream):
                self.handle_stream_response(response)
            else:
                self.handle_response(response)
        except Exception as e:
            self.response_signal.emit(str(e), self.stream)

    def get_response(self, openai_arg):
        response = self.openai.chat.completions.create(**openai_arg)
        return response

    def set_force_stop(self, force_stop):
        self.force_stop = force_stop

    def handle_response(self, response):
        if self.force_stop:
            self.finish_run(response.model, Constants.FORCE_STOP, self.stream)
        else:
            result = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            self.response_signal.emit(result, self.stream)
            self.finish_run(response.model, finish_reason, self.stream)

    def handle_stream_response(self, response):
        for chunk in response:
            if self.force_stop:
                self.finish_run(chunk.model, Constants.FORCE_STOP, self.stream)
                break
            else:
                result = chunk.choices[0].delta.content
                if result:
                    self.response_signal.emit(result, self.stream)
                else:
                    finish_reason = chunk.choices[0].finish_reason
                    if finish_reason is not None:
                        self.finish_run(chunk.model, finish_reason, self.stream)

    def finish_run(self, model, finish_reason, stream):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.response_finished_signal.emit(model, finish_reason, elapsed_time, stream)
