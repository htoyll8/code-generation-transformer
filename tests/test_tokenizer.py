import unittest
from transformers import GPT2Tokenizer

class TokenizerTestCase(unittest.TestCase):
    def setUp(self):
        self.tokenizer_file = "tokenizer"
        self.text = "Hello, world!"
    
    def test_tokenizer(self):
        # Load the trained tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained(self.tokenizer_file)

        # Add special tokens
        special_tokens = {
            "eos_token": "</s>",
            "bos_token": "<s>",
            "unk_token": "<unk>",
            "pad_token": "<pad>",
            "mask_token": "<mask>"
        }
        tokenizer.add_tokens(special_tokens, special_tokens=True)

        # Encode the text
        encoded = tokenizer.encode(self.text)

        # Decode the encoded text
        decoded = tokenizer.decode(encoded)

        self.assertEqual(self.text, decoded)