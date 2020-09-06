import re
from selenium import webdriver
from termcolor import cprint
import time
from selenium.webdriver.common.keys import Keys

class Main():
    def __init__(self):
        cprint('[*] Program başlatılıyor...','yellow')
        self.startBrowser()
        self.login()
        target = input("Takipçileri incelenecek takip ettiğiniz kişinin kullanıcı adını giriniz: ")
        self.goTarget(target)
        followersList = self.getFollowers(target)
        self.goFollowersProfile(followersList)


    def startBrowser(self):
        driver_path = "lib\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        cprint('[+] Tarayıcı başlatıldı', 'green')

    def login(self):
        cprint('[*] Giriş yapılıyor...', 'yellow')

        self.browser.get('https://instagram.com/accounts/login')
        username = input("Kullanıcı Adı: ")
        password = input("Şifre: ")

        username_page = self.browser.find_element_by_name("username")
        password_page = self.browser.find_element_by_name("password")
        username_page.send_keys(username)
        password_page.send_keys(password)
        loginBtn = self.browser.find_element_by_xpath("// *[ @ id = 'loginForm'] / div / div[3] / button / div")
        loginBtn.click()
        time.sleep(3)

        self.browser.get('https://instagram.com/')
        time.sleep(2)
        cprint('[+] Giriş yapıldı..', 'green')

    def goTarget(self,target):
        self.browser.get("https://instagram.com/"+target)
        cprint(('[+] '+ target +' kişisinin hesabına ulaşıldı.'), 'green')
        time.sleep(2)

    def getFollowers(self,target):
        numFollowers = (self.browser.find_element_by_xpath("//li[2]/a/span").text)
        numFollowings = int(self.browser.find_element_by_xpath("//li[3]/a/span").text)
        print(target+"'in takipçi sayısı: " + (numFollowers))
        print((target+"'in takip ettiği kişi sayısı: " + str(numFollowings)))
        followersLink = self.browser.find_element_by_css_selector(' #react-root > section > main > div > header > section > ul > li:nth-child(2) > a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        followersList.click()


        incelenecekTakipciSay = int(input("Kaç takipçiyi incelemek istiyorsunuz?: "))
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowersInList < incelenecekTakipciSay):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            followersList.click()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))


        count = 1
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            countPrint = "{}. takipçi: ".format(count)
            cprint(countPrint + userLink, 'blue'.format(count))
            count += 1
            followers.append(userLink)
            if (len(followers) == numFollowers):
                break
        return followers

    def goFollowersProfile(self,followersList):

        for follower in followersList:
            self.browser.get(follower)
            time.sleep(2)
            cprint(follower+"'in profiline ulaşıldı","green")

            if "This Account is Private" in self.browser.page_source:
                followings = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/span/span").text
                if ',' or '.' or 'k' or 'm' in followings:
                    followings = followings.replace(',', '')
                    followings = followings.replace('.', '')
                    followings = followings.replace('k', '')
                    followings = followings.replace('m', '000000')
                followers = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/span/span").text
                if ',' or '.' or 'k' or 'm' in followers:
                    followers = followers.replace(',', '')
                    followers = followers.replace('.', '')
                    followers = followers.replace('k', '000')
                    followers = followers.replace('m', '000000')
                time.sleep(1)

            else:
                # Takip ve takipçi sayıları çekilir
                followings = self.browser.find_element_by_xpath("//li[3]/a/span").text
                if ',' or '.' or 'k' or 'm' in followings:
                    followings = followings.replace(',', '')
                    followings = followings.replace('.', '')
                    followings = followings.replace('k', '')
                    followings = followings.replace('m', '000000')
                followers = self.browser.find_element_by_xpath("//li[2]/a/span").text
                if ',' or '.' or 'k' or 'm' in followers:
                    followers = followers.replace(',', '')
                    followers = followers.replace('.', '')
                    followers = followers.replace('k', '000')
                    followers = followers.replace('m', '000000')
                time.sleep(1)

            followers = int(followers)
            followings = int(followings)
            ratio = followings / followers


            if 0 < ratio < 0.1:
                print(follower + " 'in geri takip olasılığı %0")

            elif 0.1 < ratio < 0.5:
                print(follower + " 'in geri takip olasılığı %30")

            elif 0.5 <= ratio <= 1.4:
                print(follower + " 'in geri takip olasılığı %50")
            elif 1.4 < ratio:
                print(follower + " 'in geri takip olasılığı %70 ve üzeri")
                cprint("[+] "+follower +" %70 ve üzeri gt oranına sahip. Takip ediliyor...","green")
                self.follow(follower)

    def follow(self, follower):
        pattern = ".com/(.*?)/"
        username = re.search(pattern, follower).group(1)
        print("Kullanıcı: " + username)
        # Gizli Hesap Takibi
        if "This Account is Private" in self.browser.page_source:
            follow_div = self.browser.find_element_by_css_selector("div.BY3EC")
            follow_btn = follow_div.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/button")

            if follow_btn.text == 'Follow' or follow_btn.text == 'Follow Back':
                follow_btn.click()
                print("{} kullanıcısına başarıyla takip isteği gönderildi.".format(username))

            elif follow_btn.text == 'Requested':
                print("{} kullancısına zaten takip isteği gönderilmiş.".format(username))

            else:
                print("{} kullancısı zaten takip ediliyor".format(username))

        # Herkese açık hesap takibi
        else:
            follow_btn = self.browser.find_element_by_css_selector("button._5f5mN")
            if follow_btn.text == 'Follow' or follow_btn.text == 'Follow Back':
                follow_btn.click()
                print("{} kullanıcısı başarıyla takip edilmeye başlandı.".format(username))

            else:
                print("{} kullancısı zaten takip ediliyor".format(username))
        time.sleep(1.5)


run = Main()