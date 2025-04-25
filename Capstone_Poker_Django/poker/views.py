from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import poker
import importlib, importlib.util, sys, io, inspect
from . import bots as bots_dir
from django.shortcuts import redirect
from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
import time
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .pokerstrat import discoverStrats
from django.http import StreamingHttpResponse
import mimetypes
from wsgiref.util import FileWrapper
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from poker.forms import StudentBotForm
from poker.forms import TournamentDataForm
from poker.forms import BaseBotForm
from .models import StudentBot
from .models import BaseBot
from .models import TournamentData
from .models import Tournament
from django.db.models import Max
from django.db.models import Min
import importlib
import inspect
from .pokerstrat import Strategy
from django.core.files.storage import default_storage

def index(request):
                
    if request.method == 'POST'and request.FILES['bot1'].name.endswith('.py'):
        uploaded_file = request.FILES['bot1']
        fs= FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        return render(request, 'game_choice.html')
    return render(request, 'upload_test.html')

def gamechoice(request):
   return render(request, 'game_choice.html')

def logtest(request):
    return render(request,'index.html')
def game(request):
    botnumber = request.POST.get('botnumber', '4')  # defaults to '4'
    output = poker.run_game(botnumber=botnumber, smallblind=10, stack=1000)
    return render(request, 'log.html', {'log': output})



def custom(request):
    discovered = discoverStrats(bots_dir)
    strategy_names = [cls.__name__ for cls in discovered]
    return render(request, 'custom.html', {'strategy_names': strategy_names})

def customgame(request):
    discovered = discoverStrats(bots_dir)
    strategy_names = [cls.__name__ for cls in discovered]
    custom_config = {}
    for strat in strategy_names:
        count_str = request.POST.get(strat, '0')
        count = int(count_str) if count_str.isdigit() else 0
        if count > 0:
            custom_config[strat] = count

    smallblind = request.POST.get('smallBlind', '10') # defaults to '4'
    stacknumber = request.POST.get('stacknumber', '1000') # defaults to '4'

    output = poker.run_game(
        custom_config=custom_config,
        smallblind=smallblind,
        stack=stacknumber
    )
    return render(request, 'log.html', {'log': output})


    # Wrap output in <pre> tags to maintain formatting.
    #return HttpResponse(f"<pre>{output}</pre>")

def download(request):
    base= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name="/poker/Poker_Bot_Template.py"
    filepath= base+file_name
    thefile= filepath
    file_name= os.path.basename(thefile)
    response= StreamingHttpResponse(FileWrapper(open(thefile, 'rb'),8192),
                                    content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = "Attachment;filename=%s"% file_name
    return response

def logtext(request):
    log = request.POST.get("gamelog")
    response= HttpResponse(log,content_type='text/plain')
    response['Content-Disposition'] = 'Attachment;filename="logoutput.txt"'
    return response

def admin_check(user):
    return user.is_superuser

@login_required
def profile(request):
   
        bots = BaseBot.objects.all()
        studentbots= StudentBot.objects.filter(user=request.user).order_by('uploaded_at')
        studentBotsOrdered=studentbots.reverse()
        if request.method == 'POST':
            bot= StudentBotForm(request.POST,request.FILES)
            if bot.is_valid():
                model_instance = bot.save(commit=False)
                if model_instance.user_id is None:
                     model_instance.user_id = "1"
                model_instance.user=  request.user
                model_instance.save()
              
            else:
                context={"bots": bot}
                return render(request, 'profile.html',context)
        context={"bots": BaseBotForm(), "botlist": bots, "studentbots":studentBotsOrdered}
        return render(request, 'profile.html',context)

def profilechoice(request):
    if request.user.is_superuser:
         return redirect(reverse('adminprofile'))
    else:
         return redirect(reverse('profile'))

@login_required
@user_passes_test(admin_check)
def adminprofile(request):
        
        seen= set()
        LATEST_BOT = StudentBot.objects.values('user_id')
        bots = []
        for bot in LATEST_BOT:
            recent_bot= StudentBot.objects.filter(user_id=bot['user_id']).latest('uploaded_at')
            if recent_bot and bot['user_id'] not in seen:
                bots.append(recent_bot)
                seen.add(bot['user_id'])
        if request.method == 'POST':
            if 1==1: #if tournament logic is valid
                pass#add tournament logic
            else:
               # context={"bots": bot} 
                #return render(request, 'admin.html',context) send data 
                pass
        context={"bots": StudentBotForm(), "botlist": bots,"tournament":TournamentDataForm()}
        # request.session.aset('botlist', context['botlist'])
        return render(request, 'admin.html',context)

@login_required
def runstudent(request):
    import io

    num_games   = 50
    num_players = 8

    base_bots   = BaseBot.objects.all()
    student_qs  = StudentBot.objects.filter(user=request.user).order_by('-uploaded_at')

    context = {
        "bots":         BaseBotForm(),
        "botlist":      base_bots,
        "studentbots":  student_qs,
        "buttonclicked": False,
        "scores":       None,
        "studentseen":  None,
        "tourney_log":  None,
        "num_games":    None,
    }

    if request.method == "POST":
        # handle new upload
        form = StudentBotForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = request.user
            inst.save()

        context["buttonclicked"] = True

        selected_base_ids    = request.POST.getlist('bot_ids')
        selected_student_ids = request.POST.getlist('studentbot_ids')

        # build the config
        custom_config = {}

        #  student bots: exec from storage 
        for sb in StudentBot.objects.filter(id__in=selected_student_ids):
            bot_info = (sb.user, sb)
            raw      = default_storage.open(sb.Bot_File.name).read().decode("utf-8")

            bot_pkg  = BaseBot.__module__.rsplit('.',1)[0] + ".bots"
            mod_name = sb.Bot_File.name.rsplit(".",1)[0]
            full_name= f"{bot_pkg}.{mod_name}"

            spec = importlib.util.spec_from_loader(full_name, loader=None)
            mod  = importlib.util.module_from_spec(spec)
            mod.__package__ = bot_pkg
            mod.__spec__    = spec
            sys.modules[full_name] = mod
            exec(raw, mod.__dict__)

            from .pokerstrat import Strategy
            for _, cls in inspect.getmembers(mod, inspect.isclass):
                if issubclass(cls, Strategy) and cls is not Strategy:
                    count, info = custom_config.get(cls.__name__, (0, bot_info))
                    custom_config[cls.__name__] = (count+1, bot_info)
                    break

        #  base bots: import locally 
        import poker.bots as bots_dir
        from .pokerstrat import Strategy
        for bb in BaseBot.objects.filter(id__in=selected_base_ids):
            bot_info   = (None, bb)
            module_ref = f"{bots_dir.__name__}.{bb.Bot_File.name[:-3]}"
            module     = importlib.import_module(module_ref)
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, Strategy) and cls is not Strategy:
                    count, info = custom_config.get(cls.__name__, (0, bot_info))
                    custom_config[cls.__name__] = (count+1, bot_info)
                    break

        if not custom_config:
            context["error"] = "No bots selected. Please select at least one bot."
        else:
            # capture any prints from the poker engine
            old_stdout = sys.stdout
            sys.stdout  = io.StringIO()
            try:
                scores, closures, tourney_log = poker.run_tournament(
                    num_games=num_games,
                    custom_config=custom_config,
                    smallblind=10,
                    stack=100,
                    game_size=num_players,
                    min_players=2
                )
            finally:
                sys.stdout = old_stdout

            # tally only the student‐uploaded bots
            studentseen = {}
            for _, (wins, info, _) in scores.items():
                _, bot_inst = info
                if isinstance(bot_inst, StudentBot):
                    studentseen[bot_inst.name] = studentseen.get(bot_inst.name, 0) + wins

            # sort wins descending
            sorted_scores = dict(
                sorted(
                    {k:v[0] for k,v in scores.items()}.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            )

            context.update({
                "scores":       sorted_scores,
                "studentseen":  studentseen,
                "tourney_log":  tourney_log,
                "num_games":    num_games,
            })

    return render(request, 'profile.html', context)


@login_required
@user_passes_test(admin_check)
def runtourney(request):
    num_games   = 50
    num_players = 8

    #  Grab each user’s latest StudentBot
    seen = set()
    latest_qs = StudentBot.objects.values('user_id')
    latest_bots = []
    for row in latest_qs:
        sb = (StudentBot.objects
              .filter(user_id=row['user_id'])
              .latest('uploaded_at'))
        if sb.user_id not in seen:
            latest_bots.append(sb)
            seen.add(sb.user_id)

    context = {
        "bots":          StudentBotForm(),
        "botlist":       latest_bots,
        "buttonclicked": False,
        "tournament":    TournamentDataForm(),
    }

    if request.method == "POST":
        form = TournamentDataForm(request.POST)
        if not form.is_valid():
            context["buttonclicked"] = True
            return render(request, 'admin.html', context)
        tourney_data = form.cleaned_data

        context["buttonclicked"] = True

        #  Which StudentBots did the admin select?
        selected_ids = request.POST.getlist('bot_ids')
        custom_config = {}

        #  Dynamically load each selected bot and build custom_config
        from .pokerstrat import Strategy
        for sb in StudentBot.objects.filter(id__in=selected_ids):
            bot_info = (sb.user, sb)
            path     = sb.Bot_File.name
            raw      = default_storage.open(path).read().decode("utf-8")

            pkg       = 'poker.bots'
            mod_name  = os.path.splitext(os.path.basename(path))[0]
            full_name = f"{pkg}.{mod_name}"
            spec      = importlib.util.spec_from_loader(full_name, loader=None)
            mod       = importlib.util.module_from_spec(spec)
            mod.__package__ = pkg
            sys.modules[full_name] = mod
            exec(raw, mod.__dict__)

            for _, cls in inspect.getmembers(mod, inspect.isclass):
                if issubclass(cls, Strategy) and cls is not Strategy:
                    count, info = custom_config.get(cls.__name__, (0, bot_info))
                    custom_config[cls.__name__] = (count + 1, bot_info)
                    break

        if not custom_config:
            context["error"] = "No bots selected."
            return render(request, 'admin.html', context)

        #  Run the tournament, capturing any print()s
        old_stdout = sys.stdout
        sys.stdout  = io.StringIO()
        try:
            scores, closures, tourney_log = poker.run_tournament(
                num_games=num_games,
                custom_config=custom_config,
                smallblind=10,
                stack=100,
                game_size=num_players,
                min_players=2
            )
        finally:
            sys.stdout = old_stdout

        #  Create the TournamentData header
        closing = closures[0]['closing_bot'] if closures else None
        td = TournamentData.objects.create(
            NumberofPlayers=num_players,
            NumberofGames=num_games,
            Notes=tourney_data.get('Notes',''),
            closing_bot=closing,
            Visible=True
        )

        # Aggregate wins & rounds _by bot instance_
        agg = {}
        for _, (wins, info, rounds) in scores.items():
            user, bot_inst = info
            if bot_inst not in agg:
                agg[bot_inst] = {"user": user, "wins": wins, "rounds": rounds}
            else:
                agg[bot_inst]["wins"]   += wins
                # rounds is the same for each seat of that bot, so leave it

        #  one Tournament row per bot
        for bot_inst, data in agg.items():
            Tournament.objects.create(
                TournamentID   = td,
                StudentID      = data["user"],
                BotID          = bot_inst,
                NumberOfRounds = num_games,         # 50 games
                NumberOfWins   = data["wins"]
            )

        sorted_scores = {
            bot.name: info["wins"]
            for bot, info in sorted(agg.items(),
                                    key=lambda x: x[1]["wins"],
                                    reverse=True)
        }

        context.update({
            "scores":        sorted_scores,
            "tournament_log": tourney_log,
            "num_games":      num_games,
        })

    return render(request, 'admin.html', context)


@login_required
def tournament_history(request):

    data_list = (TournamentData.objects
                 .filter(Visible=True)
                 .order_by('-DateRun')          # show latest first
                 .prefetch_related('tournament_set',
                                   'tournament_set__StudentID',
                                   'tournament_set__BotID'))
    return render(request, 'tournament_history.html', {'data_list': data_list})

def begin(request):
    return render(request, 'begin.html')
    

def studentsgame(request):
    return render(request, 'start.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})
    
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

def redirect_shortener(request):
    return redirect('/microsoft/to-auth-redirect/')