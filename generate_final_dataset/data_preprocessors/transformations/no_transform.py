import os
import re
from tree_sitter import Language, Parser
from typing import Union, Tuple

from data_preprocessors.language_processors import (
    PythonProcessor,
)
from data_preprocessors.transformations.transformation_base import TransformationBase


class NoTransformation(TransformationBase):
    def __init__(self, parser_path: str, language: str) -> object:
        super().__init__(parser_path, language)
        if not os.path.exists(parser_path):
            raise ValueError(
                f"Language parser does not exist at {parser_path}. Please run `setup.sh` to properly set the "
                f"environment!")
        self.lang_object = Language(parser_path, language)
        self.parser = Parser()
        self.parser.set_language(self.lang_object)
        processor_map = {
            "python": PythonProcessor.get_tokens,
        }
        self.processor = processor_map[language]


    def transform_code(
            self,
            code: Union[str, bytes],
            first_half=False
    ) -> Tuple[str, object]:
        root_node = self.parse_code(
            code=code
        )
        return_values = self.processor(
            code=code.encode(),
            root=root_node
        )
        if isinstance(return_values, tuple):
            tokens, types = return_values
        else:
            tokens, types = return_values, None
        return re.sub("[ \t\n]+", " ", " ".join(tokens)), \
               {
                   "types": types,
                   "success": True
               }
