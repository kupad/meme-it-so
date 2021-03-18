SOURCE_DIR=$1
TARGET_DIR=$2

cd "$SOURCE_DIR"
for s in `ls`; do
    echo "transferring $s"
    tar -czf - $s | pv -s $(du -sb $s | awk '{print $1}') > "$TARGET_DIR/$s.tar.gz"
done

