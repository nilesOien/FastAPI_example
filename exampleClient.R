#!/usr/bin/env Rscript

# Just to ram home the point that
# a client can be in any language, here's one
# in R.
#
# Reads from
# http://127.0.0.1:8000/listAnimalTypes
# and writes a pie chart to the file pets.png
#
# To get the library, had to :
# sudo yum install curl-devel
# and then in R :
# install.packages("httr")
# install.packages("jsonlite")

# Do the request. Accept JSON.
library(httr)
data <- httr::GET('http://127.0.0.1:8000/listAnimalTypes', accept_json())

if (data$status_code != 200){
	cat("Something went wrong\n")
	q(save='no')
}

# Parse the JSON
library(jsonlite) 
parsed_data <- content(data, "text", encoding = "UTF-8") |> fromJSON()

# parsed_data looks like this :
#   animalType num
# 1        Cat   5
# 2        Dog   4
# 3       Fish   4
# 4    Reptile   3

parsed_data

# Do the pie chart.
png('pets.png', height=500, width=500)
lbl <- paste(parsed_data$animalType, ' (', parsed_data$num, ')', sep='')
pie(parsed_data$num, labels = lbl, main="Pie Chart Available Pet Categories")

cat("Results should be in pets.png\n")

q(save='no')

