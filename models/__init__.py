from mongo_beanie.models import package, release_analytics, user

all_models = [package.Package,
              release_analytics.ReleaseAnalytics,
              user.User
              ]
