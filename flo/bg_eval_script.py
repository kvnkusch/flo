from board_generator_evaluator import BoardGeneratorEvaluator
from board_generator import bg
import json
from metric_functions import my_metric_function
import pprint


evaluator = BoardGeneratorEvaluator(my_metric_function)

results = evaluator.compare([bg], 8, 100)

def get_description(results, key):
    return [
        {'min': min([r[key] for r in result]),
         'max': max([r[key] for r in result]),
         'avg': sum([r[key] for r in result]) / len(result)}
        for result in results
    ]

times = get_description(results, 'time')
metrics = get_description(results, 'metric')
fail_counts = get_description(results, 'fail_count')

print('Times:')
pprint.pprint(times)
print('metrics')
pprint.pprint(metrics)
print('fail_counts')
pprint.pprint(fail_counts)

ts = [r['time'] for r in results[0]]
ms = [r['metric'] for r in results[0]]
fs = [r['fail_count'] for r in results[0]]

with open('results.json', 'w') as results_file:
    json.dump(results, results_file, indent=4, sort_keys=True)
