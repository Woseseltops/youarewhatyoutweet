# youarewhatyoutweet

This repo stores the source code for what one day will be visible at http://youarewhatyoutweet.science.ru.nl . It's a Django website that downloads all available tweets for a particular Twitter account, classifies it with a number of classifiers (configurable in the Django admin), and shows the result in a parallax scrolling website. The classifiers are implemented dynamically and can easily be replaced by other ones.

General dependencies:
* Django
* Twython

Dependencies for our own classifiers:
* LaMachine
* numpy, scipy, sklearn: gender, age, aggression
* https://github.com/Woseseltops/soothsayer : predictability
