# You must set $COLMAP_EXE_PATH to 
# the directory containing the COLMAP executables.
$COLMAP_EXE_PATH/dense_stereo \
  --workspace_path . \
  --workspace_format COLMAP \
  --DenseStereo.max_image_size 2000 \
  --DenseStereo.geom_consistency false
$COLMAP_EXE_PATH/dense_fuser \
  --workspace_path . \
  --workspace_format COLMAP \
  --input_type photometric \
  --output_path ./fused.ply
$COLMAP_EXE_PATH/dense_mesher \
  --input_path ./fused.ply \
  --output_path ./meshed.ply
