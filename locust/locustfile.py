from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.get("/wp-login.php")
        if response.status_code != 200:
            print(f"Failed to access login page: {response.status_code} - {response.text}")
            self.interrupt()

        login_data = {
            'log': 'admin',
            'pwd': 'admin',
            'wp-submit': 'Log In',
            'redirect_to': '/wp-admin/',
            'testcookie': '1'
        }
        response = self.client.post("/wp-login.php", data=login_data, allow_redirects=False)  # Impedir redirecionamento automático após o login
        if response.status_code != 302:  # Verificar se o código de status é um redirecionamento (302)
            print(f"Failed to login: {response.status_code} - {response.text}")
            self.interrupt()

        # Acessar o URL de redirecionamento manualmente
        redirect_url = response.headers.get('location')
        if redirect_url:
            response = self.client.get(redirect_url)
            if response.status_code != 200:
                print(f"Failed to access admin page after login: {response.status_code} - {response.text}")
                self.interrupt()
        else:
            print("Failed to get redirection URL after login.")
            self.interrupt()

    @task(1)
    def index(self):
        response = self.client.get("/")
        if response.status_code != 200:
            print(f"Failed to access homepage: {response.status_code} - {response.text}")
            self.interrupt()

    @task(2)
    def create_post(self):
        title = "New Post"
        content = "This is a new post created by Locust"
        post_data = {
            'post_title': title,
            'content': content,
            'publish': 'Publish',
        }
        response = self.client.post("/wp-admin/post-new.php", data=post_data)
        if response.status_code != 200:
            print(f"Failed to create post: {response.status_code} - {response.text}")
        else:
            print("Post created successfully.")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 15)
