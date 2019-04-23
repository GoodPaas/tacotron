'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run
through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details.
'''
import os
from text import cmudict

_pad        = '_'
_eos        = '~'
_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\'(),-.:;? '

# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in cmudict.valid_symbols]

# Export all symbols:
symbols = [_pad, _eos] + list(_characters) + _arpabet



_phones_f = open(os.path.split(os.path.realpath(__file__))[0] + '/zh_lang/phones','r');
_phones = []

_line = _phones_f.readline()
while _line:
    _line = _line.strip();
    _phones.append(_line)
    _line = _phones_f.readline()

_phones_f.close();
pinyin_symbols = [_pad, _eos] + _phones;
symbols=pinyin_symbols


pinyin_dict={}

_pinyin_to_phone_f = open(os.path.split(os.path.realpath(__file__))[0] + '/zh_lang/pinyin_to_phone.txt','r');

_line = _pinyin_to_phone_f.readline();

while _line:
    _line = _line.strip()
    _parts = _line.split('\t')
    if len(_parts) == 2:
        pinyin_dict[_parts[0].lower()] = _parts[1]
    _line = _pinyin_to_phone_f.readline();
#print(pinyin_dict)
