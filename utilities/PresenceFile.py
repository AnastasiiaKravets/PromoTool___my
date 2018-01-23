import os
import time


class PresenceFile:
    def __init__(self, path):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.pdf_count = len([file for file in os.listdir(self.path) if file.endswith(".pdf")])
        self.excel_count = len([file for file in os.listdir(self.path) if file.endswith(".xlsx")])

    def is_new_pdf_file_present(self, page_url=None):
        for i in range(10):
            pdf_list = [file for file in os.listdir(self.path) if file.endswith(".pdf")]
            if len(pdf_list) > self.pdf_count:
                delta = len(pdf_list) - self.pdf_count
                if delta > 1:
                    raise Exception("Downloaded {} PDF files instead of one from page {}".format(delta, page_url))
                self.pdf_count = len(pdf_list)
                return
            else:
                time.sleep(2)
        raise Exception("New PDF file wasn't downloaded from page {}".format(page_url))

    def is_new_excel_file_present(self, page_url=None):
        for i in range(10):
            excel_list = [file for file in os.listdir(self.path) if file.endswith(".xlsx")]
            if len(excel_list) > self.excel_count:
                delta = len(excel_list) - self.excel_count
                if delta > 1:
                    raise Exception("Downloaded {} Excel files instead of one from page {}".format(delta, page_url))
                self.excel_count = len(excel_list)
                return
            else:
                time.sleep(2)
        raise Exception("New Excel file wasn't downloaded from page {}".format(page_url))
