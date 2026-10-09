"""Quoted reasoning delimiters must survive incremental parsing."""
import unittest
from serve.frontend import OutputParser


class QuotedThinking(unittest.TestCase):
    def test_quoted_closers_and_real_boundary(self):
        cases = [
            'The template is `<think>\\n\\n</think>\\n\\n`. Continue reasoning.',
            'Example:\n```jinja\n</think>\n```\nContinue reasoning.',
            'No quoted markers here.',
        ]
        for reasoning in cases:
            raw = reasoning + '</think>\n\nVisible final answer.'
            for width in range(1, len(raw) + 1):
                with self.subTest(reasoning=reasoning, width=width):
                    parser = OutputParser(thinking=True)
                    events = []
                    for pos in range(0, len(raw), width):
                        events += parser.feed(raw[pos:pos + width])
                    events += parser.finish()
                    self.assertEqual(''.join(e.text for e in events if e.kind == 'reasoning'), reasoning)
                    self.assertEqual(''.join(e.text for e in events if e.kind == 'content'), 'Visible final answer.')


if __name__ == '__main__':
    unittest.main()
