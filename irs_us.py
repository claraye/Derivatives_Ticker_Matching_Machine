# this program is inspired by "Quantlib Python Cookbook" by Balaraman and Ballabio

from QuantLib import *
today = Date(31, December, 2018)
Settings.instance().evaluationDate = today

quotes = [SimpleQuote(2.80763/100) ]

helpers = [DepositRateHelper(QuoteHandle(quotes[0]), Period(3,Months), 3, UnitedStates(), ModifiedFollowing, False, Actual360())]

for rate, tenor in [(2.6569, 2), (2.5899, 3), (2.5682, 4), (2.5703, 5),
                    (2.5969, 6), (2.6235, 7), (2.6493, 8), (2.6828, 9),
                    (2.7084, 10), (2.7309, 11), (2.7601, 12), (2.8044, 15)]:

    quotes.append(SimpleQuote(rate/100))
    helpers.append(SwapRateHelper(QuoteHandle(quotes[-1]),
                   Period(tenor, Years), UnitedStates(),
                   Annual, Unadjusted, Thirty360(Thirty360.BondBasis),USDLibor(Period(3,Months))))

rate_curve = PiecewiseLogCubicDiscount(2, UnitedStates(), helpers, Actual365Fixed())
curve_handle = RelinkableYieldTermStructureHandle(rate_curve)


fixed_schedule = Schedule(Date(1, February, 2019), Date(1, February, 2029),
Period(1, Years), UnitedStates(), ModifiedFollowing, ModifiedFollowing,
DateGeneration.Forward, False)

floating_schedule = Schedule(Date(1, February, 2019), Date(1, February, 2029),
Period(6, Months), UnitedStates(), ModifiedFollowing, ModifiedFollowing,
DateGeneration.Forward, False)

index = USDLibor(Period(3,Months),curve_handle)
swap = VanillaSwap(VanillaSwap.Payer, 10000000.0,fixed_schedule, 2.5/100, Thirty360(), floating_schedule, index, 0.0, Actual360())

swap.setPricingEngine(DiscountingSwapEngine(curve_handle))
P0 = swap.NPV()
print("Swap NPV=", P0)