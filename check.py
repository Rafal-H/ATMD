from model_allout import full_model_out

#currently has results from bunch of sim annealing runs
res = full_model_out([29.28064935,  5.61467756 ,14.76315623 ,10.70518214])
print("range: ", res[0], "   pax: ", res[1], "   PM: ", res[2])

res = full_model_out([29.86750558,  5.62590494 ,13.58113537, 12.09939284])
print("range: ", res[0], "   pax: ", res[1], "   PM: ", res[2])

res = full_model_out([29.95621812 , 5.67586025, 14.26385772, 12.46222222])
print("range: ", res[0], "   pax: ", res[1], "   PM: ", res[2])

res = full_model_out([29.90129834 , 5.78486381 ,14.84617807 ,11.05799198])
print("range: ", res[0], "   pax: ", res[1], "   PM: ", res[2])

res = full_model_out([29.96913056 , 5.61729249 ,13.75117046, 11.9666224 ])
print("range: ", res[0], "   pax: ", res[1], "   PM: ", res[2])

res = full_model_out([29.96913056 , 5.61729249, 13.75117046, 11.9666224 ])
print("range: ", res[0], "   pax: ", res[1], "   PM: ", res[2])

#this is for result of nsga2 for single objective with pax constraint
res = full_model_out([14.260412579297942,5.594781307901177,14.982335998931505,9.00081334175731])
print("range: ", res[0], "   pax: ", res[1], "   PM: ", res[2])

#this is for result of nsga2 for single objective, no pax constraint