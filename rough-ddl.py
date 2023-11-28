# VEHICLE
# reg_number
# type - 2wheeler/4 wheeler


# TOLL
# toll_id

 
# TOLL BOOTH 
# booth_id 
# toll_id 
# direction
# primary key is (toll_id, booth_id)


# TOLL_PASS
# reg_number
# toll_id
# type
# purchased_date
# times_used
# last_used_direction


# CHARGED_EVENT
# toll_pass_id
# booth_id
# charged_price


# PASS_TYPE
# pass_type 
# vehicle_type
# price


