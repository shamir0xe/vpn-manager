#!/bin/bash
repository='git@github.com:shamir0xe/vpn-manager.git'
app_dir=`pwd`
output_dir=$app_dir/output
release_dir=$output_dir/releases
release=$(date +"%Y%m%d-%H%M%S")
new_release_dir=$release_dir/$release

echo 'Cloning repository'
[ -d $release_dir ] || mkdir -p $release_dir 
git clone --depth 1 $repository $new_release_dir --recursive

echo 'Linking Storage'
rm -rf $new_release_dir/storage
ln -nfs $app_dir/storage $new_release_dir/storage

echo 'Linking Assets'
rm -rf $new_release_dir/assets
ln -nfs $app_dir/assets $new_release_dir/assets

echo 'Linking ENV'
rm -rf $new_release_dir/configs/env.json
ln -sfn $app_dir/configs/env.json $new_release_dir/configs/env.json

echo 'Unlinking previous release'
unlink $output_dir/current

echo 'Linking current release'
ln -nfs $new_release_dir $output_dir/current
