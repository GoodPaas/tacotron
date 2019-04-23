#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 xiaominfc(武汉鸣鸾信息科技有限公司) <xiaominfc@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os
from util import audio
from text.pinyinconvert import sentence_to_pinyin
from text.symbols import pinyin_dict


# 声母韵母化bznsyp中的拼音 对一些做特殊处理
def _format_pinyin(value):
    if len(value) == 1:
        return value.lower()
    
    if value == 'IY1':
        return 'i_1'
    key = value[:-1]
    end = value[-1]
    if key in pinyin_dict:
        fpinyin = pinyin_dict[key]
        if end == '5':
            end = '0'
        fpinyin = fpinyin + '_' + end
        return fpinyin
    elif key[-1] == 'r':
        return _format_pinyin(key[:-1] + end) + ' er_0'
    else :
        print('not',value)





# 声母韵母化拼音 
def _convet_pinyin(label):
    parts = label.split(' ')
    #print(parts)
    text = ''
    for value in parts:
        if len(text) > 0:
            text = text + ' '
        text = text + _format_pinyin(value)
    return text


def build_from_path(in_dir, out_dir, num_workers=1, tqdm=lambda x: x):
    executor = ProcessPoolExecutor(max_workers=num_workers)
    futures = []
    #text_dict = _load_dict(os.path.join(in_dir,'text'))
    f = open(os.path.join(in_dir,'ProsodyLabeling/000001-010000.txt'), encoding='utf-8')
    line = f.readline()
    while line:
        parts = line.strip('\n').split('\t')
        line = f.readline()
        name = parts[0]
        label = line.strip()
        text = _convet_pinyin(label)
        wav_path = os.path.join(in_dir,'Wave/' + name + '.wav')
        #print(name,"  ",wav_path);
        futures.append(executor.submit(partial(_process_utterance, out_dir, name, wav_path, text)))
        line = f.readline()
    f.close()
    return [future.result() for future in tqdm(futures)]




def _process_utterance(out_dir, name, wav_path, text):
    wav = audio.load_wav(wav_path)
    spectrogram = audio.spectrogram(wav).astype(np.float32)
    n_frames = spectrogram.shape[1]
    mel_spectrogram = audio.melspectrogram(wav).astype(np.float32)
    spectrogram_filename = 'bznsyp-spec-%s.npy' % name
    mel_filename = 'bznsyp-mel-%s.npy' % name
    np.save(os.path.join(out_dir, spectrogram_filename), spectrogram.T, allow_pickle=False)
    np.save(os.path.join(out_dir, mel_filename), mel_spectrogram.T, allow_pickle=False)
    #text = sentence_to_pinyin(text)
    return (spectrogram_filename, mel_filename, n_frames, text)
