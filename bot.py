from selenium import webdriver
from selenium.common import exceptions
from time import sleep
from config import login_details

class Instabot:
    def __init__(self, username, password):
        self.username = username
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920,1080)
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

    def get_unfollowers(self):
        sleep(4)
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/')]".format(self.username)).click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        following = self.get_names()
        f= open("insta_following.txt","w+")
        for i in following:
            if i!='':
                f.write(i)
                f.write("\n")
        f.close()
        sleep(5)
        #sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
        followers = self.get_names()
        f= open("insta_followers.txt","w+")
        for i in followers:
            if i!='':
                f.write(i)
                f.write("\n")
        f.close()
        sleep(5)
        not_following_back = [user for user in following if user not in followers]
        f= open("insta_unfollowers.txt","w+")
        for i in not_following_back:
            if i!='':
                f.write(i)
                f.write("\n")
        f.close()
        sleep(5)
        print("No of Following : ", len(following))
        print("No of followers : ", len(followers))
        print("No of Unfollowers : ", len(not_following_back))
        print(not_following_back)

    def get_names(self):
        sleep(4)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        last_ht, ht = 0, 1
        linkslist = []
        while last_ht != ht:
            try:
                last_ht = ht
                sleep(1)
                ht = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
                links = scroll_box.find_elements_by_tag_name('a')
                for i in links:
                    linkslist.append(i.text)
            except exceptions.StaleElementReferenceException as e:
                print(e)
                pass

        #print(linkslist)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        return linkslist

if __name__=='__main__':
    ld = login_details()
    username = ld.get_username()
    password = ld.get_password()
    my_bot = Instabot(username, password)
    my_bot.get_unfollowers()