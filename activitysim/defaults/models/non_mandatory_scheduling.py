# ActivitySim
# See full license in LICENSE.txt.

import os

import orca
import pandas as pd

from activitysim import activitysim as asim
from .util.vectorize_tour_scheduling import vectorize_tour_scheduling


@orca.table()
def tdd_non_mandatory_spec(configs_dir):
    f = os.path.join(configs_dir, 'configs',
                     'tour_departure_and_duration_nonmandatory.csv')
    return asim.read_model_spec(f).fillna(0)


@orca.step()
def non_mandatory_scheduling(set_random_seed,
                             non_mandatory_tours_merged,
                             tdd_alts,
                             tdd_non_mandatory_spec,
                             chunk_size):
    """
    This model predicts the departure time and duration of each activity for
    non-mandatory tours
    """

    tours = non_mandatory_tours_merged.to_frame()

    print "Running %d non-mandatory tour scheduling choices" % len(tours)

    spec = tdd_non_mandatory_spec.to_frame()
    alts = tdd_alts.to_frame()

    choices = vectorize_tour_scheduling(tours, alts, spec, chunk_size)

    print "Choices:\n", choices.describe()

    orca.add_column(
        "non_mandatory_tours", "tour_departure_and_duration", choices)
