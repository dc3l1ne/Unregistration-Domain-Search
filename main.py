#coding=utf-8
import requests
import itertools
import string
import time
import re
import json
import threading
import traceback
from bs4 import BeautifulSoup
MaxThreads=5 #The best threads that your IP won't get banned
class DomainSearch:
	def __init__(self):
		self.list=["ac","ag","am","at","be","bz","ca","cc","ch","cm","cn","co","co.uk","cx","cz","de","dk","ec","eu","fm","fr","gs","gy","hn","im","in","io","jp","la","li","lo","me","mn","mx","nl","no","pl","pm","pw","re","sc","se","sh","so","tf","tl","tv","tw","uk","us","vc","wf","ws","yt","bar","bet","bid","bio","biz","cab","car","ceo","com","dog","eus","fit","fyi","hiv","how","ink","kim","lol","mba","men","moe","mom","net","ngo","nyc","one","ong","onl","ooo","org","pet","pro","pub","red","rip","run","sex","ski","soy","srl","tax","tel","top","uno","vet","vin","win","wtf","xxx","xyz","army","asia","auto","band","beer","best","bike","blue","buzz","cafe","camp","care","cars","casa","cash","chat","city","club","cool","date","desi","diet","fail","fans","farm","film","fish","fund","gent","gift","gold","golf","guru","haus","help","host","immo","info","jobs","kiwi","land","lgbt","life","limo","link","live","loan","love","ltda","menu","mobi","moda","name","navy","news","pics","pink","plus","porn","qpon","rent","rest","rich","sale","sarl","scot","sexy","show","site","surf","taxi","team","tech","tips","town","toys","vote","voto","wiki","wine","work","yoga","zone"]
		self.list2=['com','es','net','asia','mobi','xyz','online','rocks','global','io','guru','work','life','website','today','solutions','company','photography','space','news','directory','tv','digital','email','help','city','ph','uk','design','video','world','fashion','media','chat','services','academy','cool','coach','expert']
		self.mythreads = []
	def input(self):
		try:
			while True:
				self.type=input('Please choose a type you want to generate prefix:\n1.Int\n2.Word\n3.Both\n')
				if self.type not in range(1,4):
					print 'Please choose a correct type!\n'
				else:
					break
		except KeyboardInterrupt:
			exit()
		except:
			print 'Please input an int!'
			exit()
		try:
			length=input('Please input the length of prefix:')
		except KeyboardInterrupt:
			exit()
		except:
			print 'Please input an int!'
			exit()
		while True:
			try:
				self.tld=raw_input('\nPlease input the domain suffix or length of it:')
				self.tld=int(self.tld)
				confirm=raw_input('\nThe length of suffix you selected:%d\nIs that correct?(yes/no)'%self.tld)
				if confirm == 'yes':
					confirm=''
					return(length,1)
				else:
					confirm=''
			except ValueError:
				if self.tld not in self.list:
					if self.tld not in self.list2:
						print "The suffix '%s' hasn't been supported"%self.tld
					else:
						confirm=raw_input("\nThe suffix you selected:%s,which will use GoDaddy's API\nIs that correct?(yes/no)"%self.tld)
						if confirm == 'yes':
							self.daddy=1
							return(length,1)
						else:
							confirm=''
				else:
					confirm=raw_input('\nThe suffix you selected:%s\nIs that correct?(yes/no)'%self.tld)
					if confirm == 'yes':
						confirm=''
						return(length,0)
					else:
						confirm=''
			except KeyboardInterrupt:
				exit()
	def generate_prefix(self,length):
		assert length >= 1
		p = []
		self.start=time.time()
		print 'Generating prefix..\n'
		if self.type == 3:
			p.append(itertools.product(string.printable[:36], repeat=length))
		elif self.type == 2:
			p.append(itertools.product(string.printable[10:36], repeat=length))
		elif self.type == 1:
			p.append(itertools.product(string.printable[:10], repeat=length))
		self.temp=itertools.chain(*p)
	def runthread(self):
		print 'Start @%s'%time.strftime('%Y-%m-%d %H:%M:%S\n')
		if type(self.tld) == str:
			for domain in self.temp: #Which won't cause MemoryError
				try:
					domain=''.join(domain)
					domain=domain+'.'+self.tld
					if self.tld in self.list2:
						t=threading.Thread(target=self.test_domain_godaddy, args=(domain,))
						t.setDaemon(True)
					else:
						t=threading.Thread(target=self.test_domain, args=(domain,))
						t.setDaemon(True)
					while True:
						if(threading.active_count() < MaxThreads+1):
							t.start()
							t.join(0.5)
							break
						else:
							pass
				except KeyboardInterrupt:
					exit()
				except:
					traceback.print_exc()
		elif type(self.tld) == int:
			for suffix in self.list:
				if len(suffix) == self.tld:
					for domain in self.temp:
						try:
							domain=''.join(domain)
							domain=domain+'.'+suffix
							t=threading.Thread(target=self.test_domain, args=(domain,))
							t.setDaemon(True)
							while True:
								if(threading.active_count() < MaxThreads+1):
									t.start()
									t.join(0.5)
									break
								else:
									pass
						except KeyboardInterrupt:
							exit()
						except:
							traceback.print_exc()
		print 'Done @%s'%time.strftime('%Y-%m-%d %H:%M:%S\n')
		print 'Time consuming %s'%time.strftime('%H:%M:%S',time.localtime(time.time()-self.start))
		exit()
	def test_domain(self,domain):
		count=0
		start_data={'config':'new-main','page':0,'tracking_type':'dynamic-powerbar-search','version':4.1,'search_tracking_id':0,'keyword':domain}
		while True:
			if count != 4:
				count+=1
				try:
					if count !=1:
						print 'Retry %s %d times'%(domain,count-1)
					#Start
					start=requests.post('https://www.name.com/api/search/start',data=start_data,headers=self.headers,cookies=self.cookies,timeout=30)
					json_data=json.loads(start.content)
					search_id=json_data['search_id']
					tracking_id=json_data['search_tracking_id']
					#Poll
					poll_data={'config':'new-main','page':0,'tracking_type':'dynamic-powerbar-search','version':4.1,'search_tracking_id':tracking_id,'search_id':search_id,'person_name':0}
					poll=requests.post('https://www.name.com/api/search/poll',data=poll_data,headers=self.headers,cookies=self.cookies,timeout=30)
					json_data=json.loads(poll.content)
					if json_data["domains"][domain]['avail'] == 1:
						try:
							price=json_data["domains"][domain]['products']['sedo_domains']['price']
						except:
							try:
								price=json_data["domains"][domain]['products']['registration']['price']
							except:
								try:
									price=json_data["domains"][domain]['products']['buy_domains']['price']
								except:
									try:
										price=json_data["domains"][domain]['products']['sunrise_auction_a']['price']
									except:
										f=open('err_json.txt','a')
										f.write(poll.content+'\n\n')
										f.close
						try:
							if price:
								print '%s available!\t$%s'%(domain,price)
								f=open('available.txt','a')
								f.write('%s\t$%s\n'%(domain,price))
								f.close()
								break
						except NameError:
							print '%s available!'%(domain)
							f=open('available.txt','a')
							f.write('%s\n'%(domaine))
							f.close()
							break
					else:
						print '%s unavailable!'%domain
						break
				except KeyboardInterrupt:
					exit()
				except:
					traceback.print_exc()
					# pass #Retry 
			else:
				print 'Error at %s'%domain
				f=open('error.txt','a')
				f.write(domain+'\n')
				f.close()
				break
	def test_domain_godaddy(self,domain):
		headers = {
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'en-US;q=0.5,en;q=0.3',
						'Accept-Encoding': 'gzip, deflate, br',
						'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
						'DNT':1,
						'Connection': 'keep-alive',
						'Content-Type': 'application/x-www-form-urlencoded'
						}
		count=1
		while True:
			if count !=3:
				if count !=1:
					print 'Retry %d times %s' %(count,domain)
				try:
					data=requests.get('http://sg.godaddy.com//domainsapi/v1/search/exact?q=%s&key=dpp_search&pc=&ptl='%domain,headers=headers,cookies={'currency':'USD'},timeout=30)
					json_data=json.loads(data.text)
					if json_data['ExactMatchDomain']['AvailabilityStatus'] == 1000:
						price=json_data['Products'][0]['PriceInfo']['CurrentPriceDisplay']
						print '%s available!\t%s' %(domain,price)
						f=open('available.txt','a')
						f.write('%s\t%s\n'%(domain,price))
						f.close()
						break
					elif json_data['ExactMatchDomain']['AvailabilityStatus'] == 1001:
						print '%s unavailable!' %(domain)
						break
				except:
					count+=1
			else:
				print 'Error at %s'%domain
				f=open('error.txt','a')
				f.write(domain+'\n')
				f.close()
				break
	def get_cookie_token(self):
		while True:
			headers = {
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'en-US;q=0.5,en;q=0.3',
						'Accept-Encoding': 'gzip, deflate, br',
						'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
						'DNT':1,
						'Connection': 'keep-alive',
						'Content-Type': 'application/x-www-form-urlencoded'
						}
			data=requests.get('https://www.name.com/',headers=headers)
			c_data=data.headers['set-cookie']
			str1=re.search(r'REG_IDT=([a-z]*[0-9]*)+',c_data).group(0).replace('REG_IDT=','')
			str2=re.search(r'pmovt=([a-z]*[0-9]*)+',c_data).group(0).replace('pmovt=','')
			self.cookies={'REG_IDT':str1,'pmovt':str2}
			print '\nCookies:%s,%s'%(str1,str2)
			#Get token
			t_data=BeautifulSoup(data.content, "html.parser")
			for i in t_data.find_all('meta'):
				if i.get('name') == 'csrf-token':
					token=i.get('content')
					print 'Token:%s'%token
			self.headers={
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'en-US;q=0.5,en;q=0.3',
						'Accept-Encoding': 'gzip, deflate, br',
						'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
						'DNT':1,
						'Connection': 'keep-alive',
						'Content-Type': 'application/x-www-form-urlencoded',
						'x-csrf-token-auth':token ,
						'X-Requested-With': 'XMLHttpRequest'
						}
			time.sleep(500)
			print 'Update Cookies and Token...'
	def update_cookie_token(self):
		t=threading.Thread(target=self.get_cookie_token, args=())
		t.setDaemon(True)
		t.start()
if __name__ == "__main__":
	run=DomainSearch()
	length,daddy=run.input()
	run.generate_prefix(length)
	if not daddy:
		run.update_cookie_token() #Update cookies and token every 10 minutes
		print 'Waiting 5s to get cookies and token'
		time.sleep(5)
	else:
		print "Use Godaddy's API,no need to get cookies"
	run.runthread()
