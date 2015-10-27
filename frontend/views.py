from frontend.models import *
from frontend.serializers import *
from frontend.permissions import *
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from frontend import fabfile
from fabric.api import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from frontend.forms import *
from django.core.mail import send_mail, send_mass_mail
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import Group
from django.core import serializers
from django.contrib.auth import authenticate, login, forms
from django.contrib.auth import logout
import re
import string
import os

registration_message = 'This is an email to confirm your WebASR account has been successfully registered. Our admin staff will notify you shortly once your details have been verified.'
confirmation_message = 'Your webasr account has now been activated, go to www.webasr.org to sign in.'


"""                     --------------------- REGULAR USER HANDLING --------------------                     """


class Account(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        context = RequestContext(request,{
            'user': request.user,
        }) 
        return render(request,'frontend/account.html')

def user_edit(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    if request.method == 'POST':
        form = UserEditForm(instance=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account')
        else:
            return render(request, 'frontend/user_edit.html', {'form': form})
    if request.method == 'GET':
        form = UserEditForm(instance=request.user)
        return render(request, 'frontend/user_edit.html', {'form': form})


"""                     --------------------- ADMIN USER HANDLING --------------------                   """


class UserDetail(DetailView):
    
    model = CustomUser

    def post(self,request,pk):
        
        if not request.user.is_staff:
            return HttpResponseRedirect('/login')
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        user = CustomUser.objects.filter(pk=pk)[0]
        if 'is_staff' in request.POST:
            user.is_staff = True
            user.save()
        else:
            user.is_staff = False
            user.save()
        if 'is_active' in request.POST:
            if user.is_active == False:
                send_mail('Welcome to WebASR', confirmation_message, 'registration@webasr.com',[user.email], fail_silently=False)

            user.is_active = True
            user.save()
        else:
            user.is_active = False
            user.save()
        return HttpResponseRedirect('/user/'+pk+'/')

class ListUser(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        if not request.user.is_staff:
            return HttpResponseRedirect('/login')
        users = CustomUser.objects.all()
        template = loader.get_template('frontend/listuser.html')
        queryset = Group.objects.all()
        usernum = list((query,len(query.user_set.all())) for query in queryset)

        context = RequestContext(request, {
        'users': users,
        'queryset': queryset,
        'usernum':usernum,
        })
        return HttpResponse(template.render(context))

    def post(self,request):
        group = Group.objects.get(name=request.POST.__getitem__('group'))
        request.POST.pop('group')
        
        try:
            for i in request.POST.itervalues():

                user = CustomUser.objects.get(email=i)
                user.groups.add(group)
        except:
            pass

        return HttpResponseRedirect('/users')

class GroupPage(View):
    def get(self,request):
        if not request.user.is_staff:
            return HttpResponseRedirect('/login')

        queryset = Group.objects.all()
        queryset = list((query,len(query.user_set.all())) for query in queryset)
        form = GroupForm()

        context = {
        'form':form,
        
        'queryset':queryset
        }
        return render(request,'frontend/groups.html',context)

    def post(self,request):
        form = GroupForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/groups')
        else:
            return render(request, 'frontend/groups.html', {'form': form})

def email_group(request,pk):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login')

    if request.method == 'GET':
        form = EmailForm()
        return render(request, 'frontend/email.html',{'form':form,'pk':pk})

    if request.method == 'POST':
        form = EmailForm(request.POST)
        group = Group.objects.get(pk=pk)
        users = group.user_set.all()
        emails = users.values_list('email',flat=True)
        print emails
        
        if form.is_valid():
            for email in emails:
                    send_mail(form.cleaned_data['header'],form.cleaned_data['content'], 'admin@webasr.com', [email])
            return HttpResponseRedirect('/groups')
        else:
            return render(request, 'frontend/email.html',{'form':form,'pk':pk})

def create_group(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login')
    group = Group(name=request.POST.__getitem__('name'))
    group.save
    return HttpResponseRedirect('/users')

def delete_group(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login')
    group = Group.objects.get(name=request.POST.__getitem__('name'))
    group.delete()
    return HttpResponseRedirect('/groups')

def grouplist(request,pk):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login')
    if request.method == 'GET':
        group = Group.objects.get(pk=pk)
        template = loader.get_template('frontend/grouplist.html')
        queryset = group.user_set.all()

        context = RequestContext(request, {
        'queryset': queryset,
        })
        return HttpResponse(template.render(context))


def group_users(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login')

def ungroup_users(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login')


"""                     --------------------- SYSTEM CONTROL --------------------                    """

class SystemList(View):
    def get(self,request):
        systemlist = []
        if request.user.is_authenticated():
            for system in System.objects.all():
                if set(request.user.groups.all()).intersection(system.allowed_groups.all()) != ([]):
                    systemlist.append(system)
        return HttpResponse(render(request,'frontend/useable_systems.html',{'systemlist':systemlist,}))

class SystemDetail(DetailView):

    model = System
    def get(self,request,pk):
        if not request.user.is_staff:
            return HttpResponseRedirect('/login')
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        print self.get_object()
        template = loader.get_template('frontend/system_detail.html')
        form = SystemEditForm(instance=self.get_object())
        form.fields['allowed_groups'].initial = [('','')]
        return HttpResponse(render(request,'frontend/system_detail.html',{'form':form,'object':self.get_object()}))

    def post(self,request,pk):
        form = SystemEditForm(instance=self.get_object(),data=request.POST)
        if form.is_valid():
            new_group = form.cleaned_data.pop('allowed_groups')
            if new_group != '':
                form.save()
                view_object = self.get_object()
                view_object.allowed_groups.add(Group.objects.get(name=new_group))
                view_object.save()
                return HttpResponseRedirect('/system/'+str(view_object.pk)+'/')
            form.save()
            return HttpResponseRedirect('/systems')
        else:
            return render(request, 'frontend/system_detail.html', {'form': form,'object':self.get_object()},)

class SystemHTML(DetailView):
    model = System
    def get(self,request,pk):
        if not request.user.is_staff:
            return HttpResponseRedirect('/login')
        form = SystemHTMLForm()
        form.fields['html'].initial=self.get_object().html
        return render(request, 
            'frontend/System_HTML_edit.html', 
            {'form': form,'object':self.get_object()})
    def post(self,request,pk):
        form = SystemHTMLForm(data=request.POST)
        if form.is_valid():
            html = form.cleaned_data.get('html')
            system = self.get_object()
            system.html = html
            system.save()
            system_html = open('storage/system_html/system_'+str(pk)+'.html','w')
            system_html.write(html)
            system_html.close()
            
            return HttpResponseRedirect('/systems')
        else:
            return render(request, 'frontend/system_HTML_edit.html', {'form': form,'object':self.get_object()},)

def ungroup_system(request,pk,grp):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login')
    sys = System.objects.get(pk=pk)
    sys.allowed_groups.remove(Group.objects.get(pk=grp))
    sys.save()
    return HttpResponseRedirect('/system/'+str(pk))

def show_system(request,pk):
    return render(request, 'frontend/system_show.html', {'html':System.objects.get(pk=pk).html})

def system_delete(request,pk):
    System.objects.get(pk=pk).delete()
    return HttpResponseRedirect('/systems')

def create_system(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    if not request.user.is_staff:
            return HttpResponseRedirect('/login')
    if request.method == 'POST':
        form = SystemForm(request.POST)
        print form
        if form.is_valid():
            system = System(
            name = form.cleaned_data['name'],
            language = form.cleaned_data['language'],
            environment = form.cleaned_data['environment'],
            command = form.cleaned_data['command'],
            )
            system.save()
            return HttpResponseRedirect('/systems')
    else:
        form = SystemForm()

    systemlist = System.objects.all()
    context = RequestContext(request, {
    'form': form,
    'systemlist': systemlist,
    })

    return render(request, 'frontend/systemlist.html', context)


"""                     --------------------- PROCESS CONTROL --------------------                   """


class ListProcess(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        if not request.user.is_staff:
            return HttpResponseRedirect('/login')

        processes = Process.objects.all()
        template = loader.get_template('frontend/processes.html')
        context = RequestContext(request, {
        'processes': processes,
        })
        return HttpResponse(template.render(context))
def process_delete(pk):
    process = Process.objects.get(pk=pk)
    process_ids = ProcessId.objects.filter(process=process)
    for process_id in process_ids:
        process_id.delete()
    process.delete()

def process_delete_view(request,pk):
    process_delete(pk)
    process = Process.objects.get(pk=pk)
    upload = process.upload
    upload.status = 'Aborted'
    upload.save()
    return HttpResponseRedirect('/processes')


"""                     --------------------- UPLOAD HANDLING --------------------                   """


def download(request,pk):
    if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
    upload = Upload.objects.filter(pk=pk)
    response = HttpResponse(upload[0].transcripts, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename='+upload[0].created.isoformat()+'_Transcript.zip'
    return response

class UploadDetail(DetailView):
    model = Upload
     
    def get(self,request,pk):

        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        template = loader.get_template('frontend/upload_detail.html')
        audiofiles = []
        for audiofile in Audiofile.objects.filter(upload = self.get_object()):
            file_start = '([^/]*\.wav)'
            file_regex = re.compile(file_start,re.IGNORECASE|re.DOTALL)
            file_search = file_regex.search(audiofile.audiofile.url)
            if file_search:
                audiofiles.append(file_search.group(1))
        return HttpResponse(render(request,'frontend/upload_detail.html',{'audiofiles':audiofiles,'object':self.get_object()}))

class UpdateUpload(View):
    def post(self,request):
        
        transcript = request.FILES.__getitem__('upload')
        userpk = request.POST.__getitem__('source').lstrip('0')
        
        session = request.POST.__getitem__('session')
        user = CustomUser.objects.filter(pk=userpk)
        
        uploads = Upload.objects.filter(user=user)

        for upload in uploads:
            timestamp = ''.join(i for i in upload.created.isoformat() if i.isdigit())
            
            if timestamp == session:
                upload.transcripts = transcript
                upload.save()
                process = Process.objects.get(upload=upload)
                process_delete(process.pk)
                return HttpResponse('success\n')
        return HttpResponse('failure\n')

def uploadlist(request,pk):
    if not (request.user.is_staff or request.user.pk == pk):
            return HttpResponseRedirect('/login')
    

    uploadlist = Upload.objects.filter(user=CustomUser.objects.get(pk=pk))
    uploads = []
    for upload in uploadlist:
        files = []
        for audiofile in Audiofile.objects.filter(upload = upload):
            file_start = '([^/]*\.wav)'
            file_regex = re.compile(file_start,re.IGNORECASE|re.DOTALL)
            file_search = file_regex.search(audiofile.audiofile.url)
            if file_search:
                files.append(file_search.group(1))
        uploads.append((upload,files))
    context = RequestContext(request, {
    
    'uploads': list(reversed(uploads)),
    'upload_user': CustomUser.objects.get(pk=pk)
    })
    return render(request, 'frontend/uploadlist.html', context)

class CreateUpload(View):

    @csrf_exempt
    def post(self,request):

        form = UploadForm(data=request.POST)

        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')

        if not request.FILES:
            print
            return HttpResponse('/newupload')
            
        if not 'file1' in request.FILES:
            return HttpResponse('/newupload')


        
        elif form.is_valid():
            upload = Upload(
                user = request.user,
                language = form.cleaned_data['language'],
                environment = form.cleaned_data['environment'],
                systems = form.cleaned_data['systems'],
            )

            if form.cleaned_data['metadata']:
                upload.metadata = form.cleaned_data['metadata']
                request.FILES.pop('metadata')

            upload.save()

            localpaths = []

            print request.FILES

            for x in range(1,(len(request.FILES)+1)):
                try:
                    audioupload = Audiofile(audiofile = request.FILES.__getitem__('file'+str(x)), upload = upload)
                    audioupload.save()
                    localpaths.append(audioupload.audiofile.url)
                except:
                    pass

            message = Audiofile.objects.all()
            user = request.user
            system = upload.systems
            
            pk = str(CustomUser.objects.get(email=user).id)
            n = 5 - len(pk)
            pk =  ('0' * n) + pk

            command = System.objects.get(name=system).command
           
            timestamp = ''.join(i for i in upload.created.isoformat() if i.isdigit())
            filename = 'src-'+pk+'_ses-'+timestamp

            fabfile.process_execute(localpaths,filename,command)

            process = Process(source=pk,session=timestamp,upload=upload)
            process.save()
            
            return HttpResponseRedirect('/newupload')

        else:
            systemObjects = System.objects.all()
            languages = set()
            systems = set()
            environments = set()
            for system in System.objects.all():
                languages.add(system.language)
                systems.add(system.name)
                environments.add(system.environment)
            context = RequestContext(request, {
            'languages': languages,
            'systems': systems,
            'environments': environments,
            'systemObjects': systemObjects,
            'form':form,
            })
            return render(request, 'frontend/newupload.html', context)  

        return HttpResponse(message)
    
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        form = UploadForm()
        
        system_list = set()

        
        for group in request.user.groups.all():
            for system in group.system_set.all():
                system_list.add((system.name,system.name))

        system_list.add(('',''))
      
        form.fields['systems'].choices = system_list
        systemObjects = System.objects.all()
        languages = set()
        systems = set()
        environments = set()
        for system in System.objects.all():
            languages.add(system.language)
            systems.add(system.name)
            environments.add(system.environment)
        template = loader.get_template('frontend/newupload.html')
        context = RequestContext(request, {
        'languages': languages,
        'systems': systems,
        'environments': environments,
        'systemObjects': systemObjects,
        'form':form,
        })
        return HttpResponse(template.render(context))


"""                     --------------------- AUTHENTICATION --------------------                    """


def user_login(request):
    if request.method == 'POST':
        form = forms.AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return HttpResponseRedirect('/newupload')
    else:
        form = forms.AuthenticationForm()
    systems = []
    for system in System.objects.all():
        if Group.objects.get(name='basic_system') in system.allowed_groups.all():
           systems.append(system)
	    
	news = NewsEntry.objects.all()[0].html

    return render(request, 'frontend/authentication.html', {'form': form, 'systemlist':systems, 'news':news,})

class Authentication(View):
    def get(self,request):

        return HttpResponseRedirect('/login')

class Logout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/login')


"""                     --------------------- REGISTRATION --------------------                      """
 

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            
            email = [form.instance.email]
            send_mail('Welcome to WebASR', registration_message, 'registration@webasr.com',email, fail_silently=False)

            admins = CustomUser.objects.filter(is_staff=True)
            emails = [o.email for o in admins]
            admin_message = 'New User: '+email[0]+' has registered.'
            send_mail('New User Registered', admin_message, 'registration@webasr.com', emails, fail_silently=False)
            
            return HttpResponseRedirect('/success')
    else:
        form = UserCreationForm()

    return render(request, 'frontend/register.html', {'form': form})

class RegistrationSuccess(View):
    def get(self,request):
        return render(request,'frontend/registration_success.html')


"""                     --------------------- INFORMATION PAGES --------------------                     """


class About(View):
    def get(self,request):
        return render(request,'frontend/about.html')
class News(View):
    def get(self,request):
        return render(request,'frontend/news.html')
class Conditions(View):
    def get(self,request):
        return render(request,'frontend/conditions.html')
class Projects(View):
    def get(self,request):
        return render(request,'frontend/projects.html')
class Research(View):
    def get(self,request):
        return render(request,'frontend/research.html')
class Publications(View):
    def get(self,request):
        return render(request,'frontend/publications.html')
