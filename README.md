# Lithography GDSII format generator

This program is meant to generate pillar and grid structures for being used in photo-lithography process. It allows the user to 
use different sizes of (100)Si wafers. Wafers can be subdivided into different sections that will allow the creation of different
patterns within the same wafer. The final result is a 3 layer .gds file where the first layer is the wafer, the second layer is 
working area (determined by a chosen margin) and the third layer is where the generated structures are.    


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to use this program you need:

* numpy (v1.11.0)
* gdspy (v1.1.2)

Installing numpy:

```
pip install numpy==1.11.0
```

Installing gdspy:

```
pip install gdspy==1.1.2
```

If it gives you some writing error you might want to execute these commands as sudo

### Installing

Clone the repository:

```
git clone https://github.com/mgarc729/lithography-GDSII-format-generator.git
```

Install the prerequisites and execute: 

```
chmod 554 install.sh 
```
```
./install.sh
```

To execute the program run:

```
./run.sh
```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/mgarc729/lithography-GDSII-format-generator/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/)  

## Authors

* **Manuel Garcia** - *Initial work* - [mgarc792](https://github.com/mgarc729)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* 
*
