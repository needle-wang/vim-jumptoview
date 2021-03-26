#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2016年 04月 15日 星期五 16:23:21 CST

import os.path as p
import re

# TODO, use pathlib.
SINGLE = "'"
DOUBLE = '"'


def get_view_from_url(line, settings):
  def build_file(file_to_grep, cur_dir=p.dirname(settings['buffername'])):
    tmp = p.join(cur_dir, file_to_grep)
    if p.exists(tmp):
      return tmp
    # 先判断tmp, 再看cur_dir, p.dirname('simplefile.py') == ''
    if not cur_dir or cur_dir == '/':
      raise Exception('%s not found.' % p.basename(file_to_grep))
    return build_file(file_to_grep, p.dirname(cur_dir))

  def get_vim_cmd(func_name, file_to_grep):
    return settings['grep'] + r" /\(def\|class\) \+" + func_name + "/g " + build_file(
      file_to_grep) + ' | normal jzz'

  def find_quote(oneline):
    for an_alpha in oneline:
      if an_alpha == SINGLE:
        return SINGLE
        break
      elif an_alpha == DOUBLE:
        return DOUBLE
        break

  def prune_re(oneline, quote_id):
    re_tmp = r".*?%s.*?[^\\]?%s *".replace("%s", quote_id)
    return re.sub(re_tmp, '', oneline, 1)

  vim_cmd = 'echo "sorry, i tried~"'
  quote_id = find_quote(line)
  if not quote_id:  # if cursor is not at right line.
    return 'echo'

  line = prune_re(line, quote_id)
  # 根据逗号, 找到在中间的view_str
  view_str_with_space = line.split(',')[1]
  if view_str_with_space.strip() == 'direct_to_template':
    template = re.sub(r'''('|"|}\)?$)''', '',
                      line.split(',')[2].split(':')[1].strip())
    file_name = build_file(p.join(settings['templates'], template))
    vim_cmd = '%s %s' % (settings['open'], file_name)
  else:
    # 根据引号, 分隔出一个list: [view的左边, view_str, view的右边]
    list_parsed = view_str_with_space.split(find_quote(view_str_with_space))
    try:
      view_str = list_parsed[1].strip()
    except Exception as e:
      return '''echo "can't find the view. Is it a str wrapped by quote?"'''

    if not view_str:
      return '''echo "sorry, can't do with the re contained ', or \\","'''

    view_str_separated = view_str.split('.')
    if 'include(' in list_parsed[0]:
      file_name = build_file(
        p.join(settings['prefix'], ('/'.join(view_str_separated) + ".py")))
      vim_cmd = '%s %s' % (settings['open'], file_name)
    else:
      module_name = view_str_separated[:-1]
      func_name = view_str_separated[-1]
      vim_cmd = get_vim_cmd(
        func_name, p.join(settings['prefix'], ('/'.join(module_name) + ".py")))
  return vim_cmd
