To Create Virtual Environment
python -m venv venv

To Activate Environment
.\venv\Scripts\activate



daphne django_project.asgi:application
uvicorn django_project.asgi:application


sudo systemctl restart daphne
sudo systemctl restart nginx
sudo systemctl daemon-reload


sudo systemctl restart daphne
sudo systemctl restart daphne.service

# Github
git status
git branch

If you're using the command line or Git, you can check the URL of the remote repository by running the following command:
git remote -v
git merge --abort



git init
git remote add origin https://github.com/username/repo-name.git

git clone https://<username>:<access-token>@github.com/username/repo-name.git



git config --global user.name "Your Personal Name"
git config --global user.email "yourpersonal@email.com"



git commit -m --author="harshchouhan22" -m "added pop-up on status update button "
