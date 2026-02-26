#
# You are working for a railway company that monitors the condition of its tracks using an array of sensors placed at regular
# intervals along the tracks.Each sensor records a numerical value representing the track condition at its location.
# A higher value indicates better track conditions, while lower values may signal potential issues.
# Your task is to analyze the sensor data to ensure optimal maintenance scheduling.
# Specifically, you need to identify segments of the track where the condition is consistently good over a sequence of sensors,
# but with the added requirement that these sensors report distinct readings to ensure a diverse range of conditions is being monitored.
#
# System Design round
# Past Scenario based question -
#
# Design a system to track containers through the rail network. Expanding on design to make it faster and fault tolerant.
# And here is another prompt that another candidate had:
# In trains, we have sensors that measure the distance from the train to the rail.At any point that we have a difference in the
# sensor readings we want to identify them.We currently have two sensors that provide these readings.When the two sensors do not have
# the same value, there is an error and we need to provide an alert on this error.
#
# Example:
# S1 = [1, 2, 4, 5, 5, 5, 6, 2, 2, 2, 2]
# S2 = [1, 2, 4, 4, 5, 5, 6, 2, 2, 1, 2]
# Errors = [3, 9]
