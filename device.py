import argparse
import boto3
import os
import time
import uuid
import zipfile

# Setting up AWS S3 client
s3_client = boto3.client('s3')

def upload_images(bucket_name, image_paths):
    """
    Uploads each image to the specified S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        image_paths (list): List of paths to the images to be uploaded.
    """
    try:
        for image_path in image_paths:
            file_name = os.path.basename(image_path)
            s3_client.upload_file(image_path, bucket_name, file_name)
            print(f"Uploaded {file_name} to {bucket_name}.")
            time.sleep(1)  # Delay between uploads
    except Exception as e:
        print(f"Error uploading image: {str(e)}")

def get_image_paths(directory):
    """
    Generates a list of valid image paths within the given directory.

    Args:
        directory (str): The directory to scan for images.

    Returns:
        list: A list of full paths to the images.
    """
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def unzip_images(zip_file, destination):
    """
    Unzips the specified zip file to the destination directory.

    Args:
        zip_file (str): Path to the zip file.
        destination (str): Destination directory for the unzipped files.
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)
    print(f"Unzipped {zip_file} to {destination}.")

def main():
    """
    Main function executing the script steps.
    """
    parser = argparse.ArgumentParser(description='Upload images to S3 bucket.')
    parser.add_argument('directory', type=str, help='Directory containing images.')
    args = parser.parse_args()

    # Unzip images if Images.zip is present
    zip_file = os.path.join(args.directory, 'Images.zip')
    if os.path.exists(zip_file):
        unzip_images(zip_file, args.directory)

    # Retrieving image paths and uploading to S3
    image_paths = get_image_paths(args.directory)
    bucket_name = 'store-device-images-s2110849'

    upload_images(bucket_name, image_paths)

if __name__ == '__main__':
    main()
