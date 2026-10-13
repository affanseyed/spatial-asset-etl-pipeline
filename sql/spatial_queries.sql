-- 1. Infrastructure Summary & Asset Condition Breakdown
SELECT 
    asset_type,
    COUNT(asset_id) AS total_assets,
    ROUND(SUM(length_meters)::numeric / 1000.0, 2) AS total_km,
    ROUND(AVG(condition_score)::numeric, 1) AS avg_condition_score
FROM public.municipal_road_assets
GROUP BY asset_type
ORDER BY total_km DESC;

-- 2. Spatial Proximity Analysis (PostGIS ST_DWithin)
SELECT 
    asset_id,
    asset_type,
    ROUND(ST_Distance(
        geometry, 
        ST_Transform(ST_SetSRID(ST_MakePoint(55.2744, 25.1972), 4326), 32640)
    )::numeric, 2) AS distance_to_center_m
FROM public.municipal_road_assets
WHERE ST_DWithin(
    geometry,
    ST_Transform(ST_SetSRID(ST_MakePoint(55.2744, 25.1972), 4326), 32640),
    500
);