from core.models import Profile
from django.db.models.query import QuerySet
from collections import defaultdict

from pandas import DataFrame
from sklearn.neighbors import NearestNeighbors
from core.models import Component

K_NEIGH: int = 2
MAX_SUGGESTED: int = 10
SUGGESTED_THRESHOLD: float = 0.3

def get_stars_vector(profile: Profile) -> dict[int, list[int]]:
  stars_pks = profile.stars.values_list('pk', flat=True)
  stars_dict = {pk: 1 for pk in stars_pks}
  return stars_dict

def get_neighbor_users(profiles: QuerySet[Profile], sample_profile: Profile, k: int) -> list:
  sparse_users_stars = defaultdict(list)

  # Get a high dimensinal sparse vec, represented
  # as dictionary for each user
  for p in profiles:
    sparse_users_stars[p] = get_stars_vector(p)
  
  # Add the sample user itself to make the DF turn the right size
  sparse_users_stars[sample_profile] = get_stars_vector(sample_profile)
  df = DataFrame(data=sparse_users_stars, dtype='Int8').fillna(0)
  
  # Extract sample vector (stars vector) from DF and
  # delete it from DF; otherwise, the user itself would be
  # the nearest neighbor
  sample_vector = df[sample_profile]
  df = df.drop(sample_profile, axis=1)

  # Compute k nearest neighbors with kd-tree
  neigh = NearestNeighbors(n_neighbors=k, algorithm='kd_tree')
  neigh.fit(df.T)
  neighbors = neigh.kneighbors([sample_vector])

  get_r = lambda n: df.T.iloc[n]
  return get_r(neighbors[1][0])


def get_suggested_items(profile: Profile):
  neigh = get_neighbor_users(Profile.objects.all(), profile, K_NEIGH)
  mean = neigh.mean()
  suggested = mean.sort_values(axis='index', ascending=False)
  suggested_clamped = suggested[suggested>SUGGESTED_THRESHOLD]
  suggested_idx = suggested_clamped.index
  return (
    Component.objects
      .filter(pk__in = suggested_idx)
      .exclude(stars__user = profile.user)
      [:MAX_SUGGESTED]
  )