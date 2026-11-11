select 
-- identifiers
cast(nullif(cast(vendorid as varchar), '') as integer) as vendor_id,
cast(nullif(cast(ratecodeid as varchar), '') as integer) as rate_code_id,
cast(nullif(cast(pulocationid as varchar), '') as integer) as pickup_location_id,
cast(nullif(cast(dolocationid as varchar), '') as integer) as dropoff_location_id,

-- timestamps
cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

-- trip_info
store_and_fwd_flag,
cast(nullif(cast(passenger_count as varchar), '') as integer) as passenger_count,
cast(nullif(cast(trip_distance as varchar), '') as double) as trip_distance,
cast(nullif(cast(trip_type as varchar), '') as integer) as trip_type,

-- payment info
fare_amount,
cast(nullif(cast(extra as varchar), '') as double) as extra,
cast(nullif(cast(mta_tax as varchar), '') as double) as mta_tax,
cast(nullif(cast(tip_amount as varchar), '') as double) as tip_amount,
cast(nullif(cast(tolls_amount as varchar), '') as double) as tolls_amount,
cast(nullif(cast(improvement_surcharge as varchar), '') as double) as improvement_surcharge,
cast(nullif(cast(total_amount as varchar), '') as double) as total_amount,
cast(nullif(cast(payment_type as varchar), '') as integer) as payment_type,
0 as ehail_fee,
cast(null as double) as congestion_surcharge

from {{source('staging', 'green_tripdata')}}
where vendorid is not null