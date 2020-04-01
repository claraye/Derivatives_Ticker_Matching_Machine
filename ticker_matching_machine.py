# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 12:21:25 2019

@author: qy
"""


import re
import jinja2
from collections import namedtuple
from itertools import chain

"""
The format is:
(ccy)(swap_type)[forward term](maturity)
Ccy can be a list of configurable currencies, eg 'us', 'eu', 'cd'...
Similarly, swap_type can be 'sw', 'ois', 'ff' etc.
Maturity can be '3m', '6m', '1y', '10y', '30y' etc
Forward term is optional, and have same format as Maturity.
"""

class TemplateBase(object):
    @classmethod
    def _flattemplate(cls):
        return '|'.join(cls.templates) if isinstance(cls.templates, (list, tuple)) else cls.templates

    @classmethod
    def jtemplate(cls):
        return jinja2.Template(cls._flattemplate())

    @classmethod
    def _vars(cls):
        if isinstance(cls.templates, (list, tuple)):
            vars = [re.findall("\{\{(\w+)\}\}+", temp) for temp in cls.templates]
            return list(chain(*vars))
        else:
            return re.findall("\{\{(\w+)\}\}+", cls.templates)

    @classmethod
    def _pattern(cls):
        vars = cls._vars()
        fills = ['(%s)' % "|".join(getattr(cls, v)) for v in vars]
        pattern = "^" + cls.jtemplate().render(dict(zip(vars, fills))) + "$"
        # print(pattern)
        return re.compile(pattern, re.I)

    @classmethod
    def matches(self, sym):
        res = self._pattern().match(sym)
        if res:
            vars = self._vars()
            matchedresults = namedtuple('matchedresults', vars)
            for i, v in enumerate(res.groups()):
                setattr(matchedresults, vars[i], v)
            f = getattr(self, 'validate', None)
            if f and not f(matchedresults):
                return False
            return matchedresults
        return False


class SwapTemplate(TemplateBase):
    templates = "{{ccy}}{{swap_type}}{{forward}}{{maturity}}"
    ccy = ['us', 'eu', 'cd', 'bp', 'jy', 'mx', 'cny']
    swap_type = ['sw', 'ois', 'ff', 'fedfund', 'xxx']
    forward = ['[0-9]+[BWMY]', '']
    maturity = ['[0-9]+[BWMY]+']


class FXTemplate(TemplateBase):
  templates = "{{ccy1}}{{ccy2}}"
  ccy1 = ['usd', 'cad', 'jpy', 'eur', 'gbp']
  ccy2 = ['usd', 'cad', 'jpy', 'eur', 'gbp']
  @staticmethod
  def validate(res):
    return res.ccy1 != res.ccy2


class MtgeTemplate(TemplateBase):
  templates = 'mtge_{{maturity}}'
  maturity = ['[0-9]+[BWMY]+']
  @staticmethod
  def validate(res):
    return int(res.maturity[:-1]) <=50


class Ticker(object):
    def __init__(self, typ, res):
        self.typ = typ
        self.fields = res._fields
        for field in self.fields:
            setattr(self, field, getattr(res, field))


REGISTRY = [('IRSwap', SwapTemplate),
            ('FX', FXTemplate), 
            ('Mtge', MtgeTemplate)]

class TickerMatcher():
  @staticmethod
  def identify_ticker(ticker):
      for typ, temp in REGISTRY:
          res = temp.matches(ticker)
          if res:
              return Ticker(typ, res)
  
  def match(self, ticker):
      res = self.identify_ticker(ticker)
      if res:
          strList = ['### %s matched successfully with %s template ###' % (ticker, res.typ)]
          for field in res.fields:
              strList.append('%s:\t%s' % (field, getattr(res, field)))
      else:
          strList = ['*** %s can NOT match with any template! ***' % ticker]

      return '\n'.join(strList)


if __name__ == '__main__':
    # Ticker Input
    matcher = TickerMatcher()
    for ticker in ('mxxxx10y', 'usois10y', 'usois10yy20y', 'bpff5y10y', 'ussw10x', 'USDEUR', 'CADJPY', 'usdusd', 'mtge_10y', 'mtge_90y'):
        s = matcher.match(ticker)
        print(s+'\n')

