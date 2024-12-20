
![Logo](./.github/logo.png)


# IoT RFID Scanner
[![OS - Linux](https://img.shields.io/badge/OS-Linux-blue?logo=linux&logoColor=white)](https://www.linux.org/ "Go to Linux homepage") 
[![Made with Python](https://img.shields.io/badge/Python->=3.8-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LiamTownsley2/Security-Access/codeql.yml?label=codeql)](https://github.com/LiamTownsley2/Security-Access/actions/workflows/codeql.yml)
[![GitHub License](https://img.shields.io/github/license/LiamTownsley2/Security-Access?cacheSeconds=120)](./LICENSE)

This project is designed for the Raspberry Pi Zero W, operating on Linux Kernel 5.10.103+. The core functionality of this project involves using an RFID (Radio Frequency Identification) scanner to read RFID tags, which could be used for access control or identity verification. The project takes advantage of the capabilities of Amazon Web Services (AWS) to extend the functionality of the local device to the cloud.

This project also includes an API that is accessible via port `5000`. Additionally, the API provides a dashboard, which can be accessed at `http://your_ip:5000/dashboard`.
## Demo

![App Demo Gif](https://via.placeholder.com/468x300?text=App+Demo+Gif)


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Tech Stack

**Application:** Python, boto3, picamera, mfrc522, Flask

**Kernel:** C


## Features

- API (hosted on port 500)
- Web Dashboard (hosted at `http://your_ip:5000/dashboard`)
- Command Line Interface
- In-built Linux Kernel Module


## Environment Variables

To run this project, you will need to add the following Environment Variables to your path or to the `.env` file.

`AWS_ACCESS_KEY_ID`

`AWS_SECRET_ACCESS_KEY`

`AWS_SESSION_TOKEN`

`AWS_REGION`

`S3_BUCKET_NAME`



## Run Locally

Clone the project

```bash
  git clone https://github.com/LiamTownsley2/CMP408-Internet-of-Things.git
```

Go to the project directory

```bash
  cd CMP408-Internet-of-Things
```

Run the setup script
```bash
  sudo -E ./startup.sh
```


## API Documentation

[API Documentation - Postman](https://cmp315.postman.co/workspace/New-Team-Workspace~ef0c1772-3d09-4444-98f4-23cfd4ed276a/collection/17093352-3ed4eabc-e8e3-4db1-9764-f164260748e8?action=share&creator=17093352)


## Acknowledgements

 - [Readme Generator - readme.so](https://readme.so/)
## License

[GNU Affero General Public License v3.0](./LICENSE)


## Authors

- [Liam Townsley (@LiamTownsley2)](https://www.github.com/LiamTownsley2)

