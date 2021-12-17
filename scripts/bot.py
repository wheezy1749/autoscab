from autoscab.deployments import Deployment

fredmeyer = Deployment.get_deployments()['fredmeyer']
bot = fredmeyer.make(headless=False)
bot.apply()
