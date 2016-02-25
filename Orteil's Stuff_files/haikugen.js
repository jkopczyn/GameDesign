Gizmo.Play=function ()
{
	String.prototype.Cap=function(){return this.charAt(0).toUpperCase()+this.slice(1);}

	Gizmo.screen=l('gizmo');
	
	Gizmo.Words1=['there','here','now','then','once','still','soon'];
	Gizmo.Words2=['sometimes','often','you see','alone','likewise','along','brisly','slowly','oddly','warmly','coldly','briefly'];
	Gizmo.Words3=['suddenly','silently','day by day','together','one by one','finally','after all','strangely','frequently','knowingly','happily','wisely','otherwise'];
	
	Gizmo.Join1=['with','from','for','on','of','through','to'];
	Gizmo.Join2=['within','above','beyond','over','inside','beneath','before','after','against'];

	Gizmo.Nouns1=['crane','toad','frog','pond','tree','leaf','fox','bull','ox','fish','bird','sun','moon','hill','sky','cloud','sea','boat','tide','wave','sand','dune','man','boy','girl','child','song','spring','fall','grove','dusk','mist','noon','road','pride','joy','world','ant','bee','dog','son','harp','flute','sound','hen','pig','stone','wasp','reed'];
	Gizmo.Nouns2=['farmer','insect','old man','mountain','ocean','river','ripple','flower','forest','thicket','master','woman','poet','village','fire','water','summer','winter','warrior','moonlight','sunlight','bamboo','morning','silence','glory','sadness','dragon','country','cricket','mother','father','daughter','music','season','spirit','monkey','statue','village','beetle'];
	Gizmo.Nouns3=['fisherman','happy man','mountain range','bamboo grove','dim sunlight','dim moonlight','traveller','musician','family','evening','happiness','universe','dragonfly','butterfly'];

	Gizmo.Verbs1=['flees','dreams','thinks','sings','swims','flies','grows','hides','hurts','calls','fades','leaps','works','lies','rests','slows','rides','sleeps','steals'];
	Gizmo.Verbs2=['beckons','follows','lifts up','answers','eats up','can\'t find','walks with','shall find','must seek','speaks to','attracts','conceals','reveals','remains','regrets','recalls','echoes','welcomes','meets with','dreams up'];

	Gizmo.Full5=['From time to time','Occasionally','Mysteriously','Over and over','Again and again','Unfathomably','As time passes by','Inexorably','I wonder sometimes','Why should it be so','Season to season','I remember when','You will one day see','Refrigerator','Haikus are silly'];

	Gizmo.Templates5=['The n1 v1 the n1','w2, the n2','w1, the n2 v1','j1 the n2\'s n1','j1 the n1\'s n2','n1 j1 the n2','f5','v2 the n1 - w1','The n2 - w2','the n1 - w3','j1 the n3','Oh, how the n1 v1','n2! n1! n2','n1! n1! n3','n1! n2! n2','n1 j2 the n1','v1 j2 the n1','w1 v1, w3','The n2 v2','w3 j2'];
	Gizmo.Templates7=['The n1, the n1 and the n1','The n2 v2 the n1','The n1 v2 the n2','The n2 w3 v1','w2 the n3 v1','w3 the n2 v1','w2, the n2 v2','w3 the n1 v2','w3 the n2 v1','And the n2 j1 the n1','n2 and n2 and n1!','j2 the n1 and n2','j2 the n2 and n1','j2 the n3 v1','From the n2 to the n1','From the n1 to the n2','The n1 v1 j2 the n1','The n1 v1 j1 the n2','v1, w3, j1 the n1','v1, w2, j2 the n1'];

	Gizmo.Generate=function()
	{
		var str='';
		str+=Choose(Gizmo.Templates5)+'|';
		str+=Choose(Gizmo.Templates7)+'|';
		str+=Choose(Gizmo.Templates5);

		var str2='';
		for (var i=0;i<str.length;i++)
		{
			str2+=str[i];
			if (i>0)
			{
				var last=str[i-1]+str[i];
				if (last=='n1') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Nouns1);}
				else if (last=='n2') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Nouns2);}
				else if (last=='n3') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Nouns3);}
				else if (last=='w1') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Words1);}
				else if (last=='w2') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Words2);}
				else if (last=='w3') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Words3);}
				else if (last=='v1') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Verbs1);}
				else if (last=='v2') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Verbs2);}
				else if (last=='f5') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Full5);}
				else if (last=='j1') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Join1);}
				else if (last=='j2') {str2=str2.slice(0,-2);str2+=Choose(Gizmo.Join2);}
			}
		}
		str=str2.split('|');
		for (var i=0;i<str.length;i++)
		{str[i]=str[i].Cap();}
		str=str.join('<br>')+'.';

		Gizmo.screen.innerHTML='<a style="bottom:2px;right:2px;text-align:right;font-size:9px;" onclick="Gizmo.Generate();">'+str+'</a>';
	}
	Gizmo.Generate();
}