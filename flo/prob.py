from numpy import random


class Distribution():
    def __init__(self, distribution):
        # [(prob, event)]
        # prob := relative probability of accompanying event
        #         probs do not need to add to 1, are normalized by default
        # event := either Distribution or terminal value
        #          if event is Distribution, its own terminal values will be
        #          chosen (using appropriate conditional probs)
        self._dist = distribution

    @staticmethod
    def uniform(events):
        return Distribution([(1, e) for e in events])

    def choice(self, verbose=False):
        flat_distribution = self._get_flat_distribution()
        if verbose:
            print(len(flat_distribution))
        if not flat_distribution:
            raise ValueError("Cannot make choice from empty distribution")
        return random.choice([e for _, e in flat_distribution],
                             p=[p for p, _ in flat_distribution])

    def _get_flat_distribution(self):
        unnormalized_flat_dist = []
        for prob, event in self._dist:
            if isinstance(event, Distribution):
                unnormalized_flat_dist += [
                    ((prob * p), e) for p, e in event._get_flat_distribution()]
            else:
                unnormalized_flat_dist.append((prob, event))

        normalization_factor = sum([p for p, _ in unnormalized_flat_dist])
        if normalization_factor == 0:
            return unnormalized_flat_dist
        else:
            return [(p / normalization_factor, e)
                    for p, e in unnormalized_flat_dist]

    def not_empty(self):
        flat_distribution = self._get_flat_distribution()
        return flat_distribution
