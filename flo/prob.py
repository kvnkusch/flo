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

    def choice(self):
        flat_distribution = self._get_flat_distribution()
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


class LazyDistribution(Distribution):
    # TODO: Improve this spec-like-thing

    # self._dist of LazyDistribution (different than Distribution)
        # [(prob, event_func)]
        # prob := relative probability of accompanying event
        #         probs do not need to add to 1, are normalized by default
        # event_func := function that returns LazyDistribtuion or terminal value
        #               if returns a LazyDistribution and event_func is chosen,
        #               choice() will return the innter LazyDistribution's choice

    @staticmethod
    def uniform(event_funcs):
        return LazyDistribution([(1, e) for e in event_funcs])

    def choice(self):
        normalization_factor = sum([p for p, _ in self._dist])
        chosen_event = random.choice([e for _, e in self._dist],
                                          p=[p / normalization_factor for p, _ in self._dist])
        if isinstance(chosen_event, Distribution):
            import pdb; pdb.set_trace()
            return chosen_event.choice()

        return chosen_event()

    def not_empty(self):
        raise NotImplementedError
