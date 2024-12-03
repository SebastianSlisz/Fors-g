#!/usr/bin/env ruby

require 'csv'
require 'json'

csv_table = CSV.read("data.csv", headers: true)
geojson = JSON.load(File.open('postal_codes.geojson'))

geojson['features'].select do |postal_code|
  row_data = csv_table.find { |r| r['postal_code'].to_s == postal_code['properties']['postal_code'].to_s }
  postal_code['properties'] = {}

  row_data.each do |header, value|
    postal_code['properties'][header] = value
  end
end


File.open('postal_codes.geojson', 'w') do |file|
  file.write(geojson.to_json)
end