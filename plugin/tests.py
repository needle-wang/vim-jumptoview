#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#2016年 04月 15日 星期五 22:43:07 CST

import os.path as p
import unittest
import mock
from jumptoview import get_view_from_url

class JumptoviewTestCase(unittest.TestCase):

  def setUp(self):
    self.settings = {}
    self.settings['open'] = "tabnew"
    self.settings['grep'] = "vimgrep"
    self.settings['templates'] = "templates"
    self.settings['buffername'] = "/www/dj_proj/dj_proj/urls.py"

  def filepath_mock(self, filepath):
    if filepath == "/www/dj_proj/dj_proj/dj_proj/views.py":
      return False
    if filepath == "/www/dj_proj/dj_proj/blog/urls.py":
      return False
    return True

  def test_get_func(self):
    self.settings['prefix'] = "dj_proj"
    with mock.patch('os.path.exists', new = self.filepath_mock):
      self.line = "url(r'^$', 'views.first_page'),"
      print get_view_from_url(self.line, self.settings)

  def test_get_app_urls(self):
    self.settings['prefix'] = "blog"
    with mock.patch('os.path.exists', new = self.filepath_mock):
      self.line = "url(r'^blog/', include('urls')),"
      print get_view_from_url(self.line, self.settings)

  def test_get_direct_template(self):
    with mock.patch('os.path.exists', new = self.filepath_mock):
      self.line = """url(r'^$', direct_to_template, {"template": "homepage.html"}, name="home"),"""
      print get_view_from_url(self.line, self.settings)


if __name__ == '__main__':
  unittest.main()
