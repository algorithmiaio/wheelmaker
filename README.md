# Algorithmia Wheel Maker

This project defines best practices and techniques on how to create a python wheel that contains C++ shared objects, along with any potental python components so that they work properly on the Algorithmia platform. For requirements, please refer to the discourse and ongoing conversation as they are subject to change.


## Compliation quirks

You must compile your C++ project in an environment that's identical to what it will be executing on as an algorithm, as most C++ projects compile using relative system paths (static builds not withstanding).
__Before continuing in this guide, you should already have terminal access to a running docker container using the provided image.__

The first step is to compile your C++ project, best practice here is to build only what you need.

Need a little help on figuring out how to compile your C++ project so that our wheel_builder will work properly? Take a look at our [caffe_builder][caffe_builder] script and see how we migrate and move necessary files while preserving the overall folder architecture.
If you're creating a simple python wrapper, exporting your `*.so` / `*.dll` / `*.pyd` files should be sufficient. An example of a project like this would be the [cv2 / opencv-python][cv2] package. It contains a simple ```__init__.py``` and a single ```cv2.so``` file, super simple!


Your project's build products should now been placed into a properly named system directory, with all of the necessary relative path heirarchies preserved. If you want to test out your package now, simply open up a python REPL (aka type in `python` into your terminal window) and simply import your package by name.

Make sure that your project's `__init__.py` imports the right components from your shared objects, otherwise importing your package will not allow you to access your compiled library. [look at this opencv example][cv2_init] for guidance.

`If there are any issues with the python repl, then something might have went wrong during the compilation / data migration stage. Don't hesistate to get in touch with us if you're having issues.`

## Wheel creation

Now we're ready to finally create a wheel with the [wheel_maker][whl_mkr] script. Make sure to rename the placeholder values at the top of the script, ensuring that your package name is identical to the folder with your build products.

Wheel construction is a simple zippping process - but pip requires that file to be of a very particular format.

To start the process, type this: `/opt/anaconda2/bin/python wheel_maker.py bdist_wheel`.

`The version of anaconda python you use is important. While building if you need any interfacing with python at all, be sure to use the implementation in the relevent anaconda bin directory.`

` When creating an algorithm, the version of python you decide to use must match the version that was created to construct the wheel. Otherwise a version mismatch exception will occur during import`

If you followed these steps and everything has worked out smoothly so far, your wheel should now exist in the `dist` directory. If you want to inspect the wheel's contents at this point, you can do so by using the `unzip` command.

## Saving the wheel

Now we've created a wheel, we've confirmed that it works - but it doesn't do us much good sitting inside of a docker container on our local machine.

We need a way to store this for the long term - S3 is a great long term storage tool. [Create an S3 bucket][aws_bucket] (algorithmia needs read access, so either restrict to VPC or make it publicly accessable for now), and either [create or obtain your aws CLI credenials][aws_creds].

Once that's done we're ready to upload our finished wheel, simply edit the placeholders in the [upload utility][upload] and execute it like so: `python upload_to_s3.py my_project_-0.1.0_cp2.whl my-wheels`.


## Using the wheel on algorithmia
Now that we have a wheel, it should work on the algorithmia platform. To test this, simply create a new python algorithm (ensuring that the version you used in creating your wheel is the same as your new algorithm), and add the S3 URL to the dependencies file.
After compiling you should be able to interact with your compiled C++ project freely within python.



[aws_bucket]: https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html
[whl_mkr]: https://github.com/algorithmiaio/wheel_maker/blob/master/wheel_maker.py
[aws_creds]: https://docs.aws.amazon.com/general/latest/gr/aws-security-credentials.html
[upload]: https://github.com/algorithmiaio/wheel_maker/blob/master/upload_to_s3.py
[caffe_builder]: https://github.com/algorithmiaio/wheel_maker/blob/master/caffe_builder.py
[cv2]: https://github.com/skvark/opencv-python
[cv2_init]: https://github.com/skvark/opencv-python/blob/master/cv2/__init__.py#L4-L5