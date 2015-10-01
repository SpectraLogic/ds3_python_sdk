require "faraday"
require "json"

# Has to be to https and not http.  Insert your blackpearl box.
connection = Faraday.new(:url => "https://sm25-2-mgmt.eng.sldomain.com",
                         # Don't worry about verifying the SSL certificate.
                         # In a production system, you'd want to verify it but
                         # it doesn't matter for the cucumber tests.
                         :ssl => { :verify => false }) do |conn|
  conn.request(:basic_auth, "spectra", "spectra")
  # User Ruby's net/http library
  conn.adapter(:net_http)
  # Setup for JSON requests and responses.  You could insert your own
  # middleware to handle the JSON parsing and encoding, which is what
  # SpectraView does.  This example just manually takes care of that down below.
  conn.headers = { "Accept" => "application/json",
                   "Content-Type" => "application/json" }
end

# List all users
response = connection.get("/users")
# All GET responses are under a root "data"
users = JSON.parse(response.body)["data"]

spectra_user = {}
users.each do | user_entry |
  spectra_user = user_entry if user_entry["name"].eql?("Spectra")
end

# None of the "/users" responses include the S3 keys.  For that, you have to
# make a separate "/s3v/keys" request which is setup to return an array
# of S3 authid/secretkey pairs in case we ever allow more than one pair per
# user.
response = connection.get("/s3v/keys?user_id=#{spectra_user["id"]}")
spectra_user_keys = JSON.parse(response.body)["data"][0]

ENV["DS3_ENDPOINT"] = "sm25-2.eng.sldomain.com"
ENV["DS3_SECRET_KEY"] = spectra_user_keys["secret_key"]
ENV["DS3_ACCESS_KEY"] = spectra_user_keys["auth_id"]
puts "DS3_ENDPOINT #{ENV["DS3_ENDPOINT"]}"
puts "DS3_SECRET_KEY #{ENV["DS3_SECRET_KEY"]}"
puts "DS3_ACCESS_KEY #{ENV["DS3_ACCESS_KEY"]}"

puts "docker run -e DS3_ENDPOINT -e DS3_SECRET_KEY -e DS3_ACCESS_KEY -it --dns=10.1.0.9 spectralogic/ds3_c_docker_test"
output = `docker run -e DS3_ENDPOINT -e DS3_SECRET_KEY -e DS3_ACCESS_KEY -it --dns=10.1.0.9 spectralogic/ds3_c_docker_test`
docker_status = $?

puts output
puts "docker status[#{docker_status}][#{docker_status.exitstatus}]"
exit docker_status.exitstatus

