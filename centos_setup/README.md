## Quick Python3.6 setup for new CentOS

Run the follow in your CentOS terminal.

```bash
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
sudo yum update -y
sudo yum install -y git
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip

sudo yum install -y python36u python36u-devel python36u-pip

sudo pip3.6 install ipython
sudo pip3.6 install tqdm
sudo yum install -y python36u-tkinter
sudo pip3.6 install matplotlib

sudo yum install -y vim

# remote debug
sudo pip3.6 install pydevd=1.5.1

# tmux
sudo yum install -y tmux

# yarn
curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
curl --silent --location https://rpm.nodesource.com/setup_12.x | sudo bash -
sudo yum install -y yarn
```
