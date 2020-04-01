# Derivatives_Ticker_Matching_Machine
A ticker matching machine using regular expression and Jinja2 for various financial product to pair with their corresponding price models.

## sample outputs:
"### mxxxx10y matched successfully with IRSwap template ###\
ccy:    mx\
swap_type:      xxx\
forward:        \
maturity:       10y"

"### usois10y matched successfully with IRSwap template ###
ccy:    us\
swap_type:      ois\
forward:        \
maturity:       10y"

"*** usois10yy20y can NOT match with any template! ***"

"### bpff5y10y matched successfully with IRSwap template ###\
ccy:    bp\
swap_type:      ff\
forward:        5y\
maturity:       10y"

"*** ussw10x can NOT match with any template! ***"

"### USDEUR matched successfully with FX template ###\
ccy1:   USD\
ccy2:   EUR

"### CADJPY matched successfully with FX template ###\
ccy1:   CAD\
ccy2:   JPY

"*** usdusd can NOT match with any template! ***"

"### mtge_10y matched successfully with Mtge template ###\
maturity:       10y"

"*** mtge_90y can NOT match with any template! ***"