import re
s=open('film2.html',encoding='utf-8').read().replace('<html lang="fr">','<html lang="en">')
import json as _j
_F=_j.load(open("fatf.json",encoding="utf-8"))
T=[("Listes du "+_F["date_fr"],"Lists of "+_F["date_en"]),("<b>Pays liés au client</b><span>1 en liste grise GAFI</span>","<b>Countries linked to the client</b><span>1 on FATF grey list</span>"),("Pièce d'identité","Identity document"),("Lecture automatique","Automatic reading"),("<small>Nom</small>","<small>Surname</small>"),("<small>Prénom</small>","<small>Given name</small>"),("<small>Date de naissance</small>","<small>Date of birth</small>"),("<small>Expire le</small>","<small>Expiry date</small>"),("✓ Pièce lue et vérifiée","✓ Document read and verified"),("<small>Base PPE</small>","<small>PEP database</small>"),("Ancien maire · mandat 2014–2020","Former mayor · term 2014–2020"),("<em>Né le 14.03.1968</em>","<em>Born 14.03.1968</em>"),(">Correspondance<",">Match<"),
("Chaque pays lié au client,<br>comparé aux listes du GAFI.","Every country linked to the client,<br>checked against FATF lists."),("Liste noire GAFI","FATF black list"),("Liste grise GAFI","FATF grey list"),("<em>· pays liés</em>","<em>· linked countries</em>"),("Siège · Helix Holdings","Head office · Helix Holdings"),("P. Durand · bénéficiaire","P. Durand · beneficial owner"),(">Contrepartie<",">Counterparty<"),("Hors listes","Not listed"),("1 pays lié en liste grise du GAFI","1 linked country on the FATF grey list"),(">Belgique<",">Belgium<"),(">Allemagne<",">Germany<"),(">Suisse<",">Switzerland<"),(">Émirats arabes unis<",">United Arab Emirates<"),
("✓ Dossier créé","✓ Matter created"),("✓ Facture réglée","✓ Invoice paid"),("Toutes vos échéances<br>au même endroit.","All your deadlines<br>in one place."),("✓ Synchronisé avec Outlook","✓ Synced with Outlook"),
(">Dossier</span><span data-a=\"13\"",">Matter</span><span data-a=\"13\""),(">Contrôles AML</span><span data-a=\"52\"",">AML checks</span><span data-a=\"52\""),(">Vigilance</span><span data-a=\"59\"",">Due diligence</span><span data-a=\"59\""),(">Facturation</span><span data-a=\"65\"",">Billing</span><span data-a=\"65\""),(">Agenda</span><span data-a=\"69.5\"",">Calendar</span><span data-a=\"69.5\""),(">Pilotage</span></div>",">Overview</span></div>"),
("<small data-at=\"0.2\">Organigramme de détention</small>","<small data-at=\"0.2\">Ownership chart</small>"),("La chaîne de détention<br>reconstituée,<br>niveau par niveau.","The ownership chain<br>rebuilt,<br>level by level."),
(">Niveau 1<",">Level 1<"),(">Niveau 2<",">Level 2<"),(">Niveau 3<",">Level 3<"),(">Niveau 4<",">Level 4<"),("Bénéficiaires effectifs identifiés","Beneficial owners identified"),
("<small data-at=\"0.2\">Niveau de vigilance</small>","<small data-at=\"0.2\">Due diligence level</small>"),("La vigilance et le suivi,<br>proposés automatiquement.","Due diligence and follow-up,<br>suggested automatically."),
("<span>Simplifiée</span><span>Standard</span><span>Renforcée</span>","<span>Simplified</span><span>Standard</span><span>Enhanced</span>"),("Vigilance renforcée proposée","Enhanced due diligence suggested"),
("<b>Personne politiquement exposée</b><span>1 correspondance</span>","<b>Politically exposed person</b><span>1 match</span>"),("<b>Bénéficiaires effectifs</b><span>3 pays</span>","<b>Beneficial owners</b><span>3 countries</span>"),
("<b>Listes de sanctions</b><span>Aucune correspondance</span>","<b>Sanctions lists</b><span>No match</span>"),("<b>Médias défavorables</b><span>Aucune information</span>","<b>Adverse media</b><span>No information</span>"),
("Plan de suivi proposé","Suggested follow-up plan"),("<b>Aujourd'hui</b><em>Ouverture du dossier</em>","<b>Today</b><em>Matter opened</em>"),("<b>Mai 2027</b><em>Revue KYC</em>","<b>May 2027</b><em>KYC review</em>"),("<b>Nov. 2027</b><em>Revue complète</em>","<b>Nov. 2027</b><em>Full review</em>"),
("Surveillance continue des listes et des médias","Ongoing monitoring of lists and media"),("Valider le plan","Approve the plan"),
("Dossiers, temps, factures, agenda, contrôles AML…","Matters, time, invoices, calendar, AML checks…"),("…répartis entre plusieurs outils.","…spread across several tools."),("Tout est réuni dans Norvy.","It all comes together in Norvy."),
("<b>Dossiers</b><em>42 actifs</em>","<b>Matters</b><em>42 active</em>"),("<b>Facturation</b><em>48 250 € ce mois</em>","<b>Billing</b><em>€48,250 this month</em>"),("<b>Agenda</b><em>2 audiences aujourd'hui</em>","<b>Calendar</b><em>2 hearings today</em>"),("<b>Contrôles AML</b><em>2 alertes à examiner</em>","<b>AML checks</b><em>2 alerts to review</em>"),
("Le client et ses bénéficiaires,<br>vérifiés dès l'ouverture.","The client and its owners,<br>checked as the matter opens."),
("3 bénéficiaires effectifs localisés","3 beneficial owners located"),
("<small data-at=\"0.2\">Listes de sanctions</small>","<small data-at=\"0.2\">Sanctions lists</small>"),("Chaque nom comparé<br>aux listes officielles.","Every name matched<br>against official lists."),
("<span>Société</span>","<span>Company</span>"),("<span>Bénéficiaire effectif</span>","<span>Beneficial owner</span>"),("✓ 0 correspondance sur 4 listes","✓ 0 matches across 4 lists"),("<em>0 correspondance</em>","<em>0 matches</em>"),

(">Dossiers</span>",">Matters</span>"),(">Tableur</span>",">Spreadsheet</span>"),(">Agenda</span><div",">Calendar</span><div"),(">E-mails</span>",">Emails</span>"),(">Outil AML</span>",">AML tool</span>"),
("<small data-at=\"0.2\">Dossiers et clients</small>","<small data-at=\"0.2\">Matters and clients</small>"),("Un dossier ouvert en quelques clics.","A matter opened in a few clicks."),
("Nouveau dossier","New matter"),("✓ Fiche complétée","✓ Record completed"),("<small>Dénomination</small>","<small>Name</small>"),("<small>Type de dossier</small><span>Droit des sociétés</span>","<small>Matter type</small><span>Corporate law</span>"),("<small>Responsable</small>","<small>Lead lawyer</small>"),
("<small data-at=\"0.2\">Contrôle AML</small>","<small data-at=\"0.2\">AML check</small>"),
("· 3 bénéficiaires effectifs","· 3 beneficial owners"),("Union européenne","European Union"),("Nations unies","United Nations"),("Royaume-Uni","United Kingdom"),("États-Unis","United States"),

("Analyse PPE","PEP analysis"),("Personnes politiquement exposées","Politically exposed persons"),("Les profils sensibles<br>repérés pour vous.","Sensitive profiles<br>flagged for you."),
("Comparaison aux bases PPE","Matching against PEP databases"),("1 correspondance à examiner","1 match to review"),("Valider le client","Approve the client"),("✓ Décision enregistrée","✓ Decision recorded"),
("<small data-at=\"0.2\">Médias défavorables</small>","<small data-at=\"0.2\">Adverse media</small>"),("La presse du monde entier,<br>passée au crible.","Press from around the world,<br>screened."),
("<span>Plusieurs langues</span>","<span>Multiple languages</span>"),("<span>Presse, sites officiels, décisions de justice</span>","<span>Press, official sites, court decisions</span>"),
("Presse internationale","International press"),("Presse régionale","Regional press"),("Sites officiels","Official sites"),("Décisions de justice","Court decisions"),("Blogs spécialisés","Specialist blogs"),
("✓ Aucune information défavorable","✓ No adverse information"),
("<small data-at=\"0.2\">Facturation</small><h2 data-at=\"0.4\">Du temps saisi à la facture.</h2>","<small data-at=\"0.2\">Billing</small><h2 data-at=\"0.4\">From recorded time to invoice.</h2>"),
("Temps · Helix Holdings","Time · Helix Holdings"),("<b>Rédaction du pacte d'associés</b>","<b>Drafting shareholders' agreement</b>"),("<span>Lun. · Me Laurent</span>","<span>Mon. · Me Laurent</span>"),("<b>Rendez-vous client</b>","<b>Client meeting</b>"),("<span>Mar. · Me Laurent</span>","<span>Tue. · Me Laurent</span>"),("<b>Relecture des statuts</b>","<b>Review of the articles</b>"),("<span>Mer. · Me Martin</span>","<span>Wed. · Me Martin</span>"),
("Créer la facture","Create the invoice"),("Facture F-2026-118 · 6 h 30","Invoice F-2026-118 · 6 h 30"),("1 625 €","€1,625"),("Envoyée le 4/11 · réglée le 14/11","Sent on 4 Nov. · paid on 14 Nov."),(">PAYÉE<",">PAID<"),
("<small data-at=\"0.2\">Agenda</small>","<small data-at=\"0.2\">Calendar</small>"),("Agenda · cette semaine","Calendar · this week"),
("<small>Lun</small>","<small>Mon</small>"),("<small>Mar</small>","<small>Tue</small>"),("<small>Mer</small>","<small>Wed</small>"),("<small>Jeu</small>","<small>Thu</small>"),("<small>Ven</small>","<small>Fri</small>"),
("9 h 30 Audience","9:30 Hearing"),("14 h Rendez-vous","2 pm Meeting"),("10 h Médiation","10 am Mediation"),("16 h Signature","4 pm Signing"),("Délai d'appel","Appeal deadline"),(">Conclusions<",">Submissions<"),("11 h Tribunal","11 am Court"),("Rappel : audience demain à 9 h 30","Reminder: hearing tomorrow at 9:30"),
("<small data-at=\"0.2\">Tableau de bord</small>","<small data-at=\"0.2\">Dashboard</small>"),("Le cabinet, d'un coup d'œil.","The firm, at a glance."),("<span class=\"ttl\">Tableau de bord</span>","<span class=\"ttl\">Dashboard</span>"),
("<small>Dossiers actifs</small>","<small>Active matters</small>"),("<em>+6 ce mois</em>","<em>+6 this month</em>"),("<small>Heures facturables</small>","<small>Billable hours</small>"),("<em>ce mois</em>","<em>this month</em>"),("<small>Encaissé</small>","<small>Collected</small>"),("<em>des factures</em>","<em>of invoices</em>"),("<small>Alertes AML</small>","<small>AML alerts</small>"),("<em>à examiner</em>","<em>to review</em>"),
("Facturé et encaissé, 6 derniers mois","Invoiced and collected, last 6 months"),("<span>Juin</span>","<span>Jun</span>"),("<span>Juil</span>","<span>Jul</span>"),("<span>Août</span>","<span>Aug</span>"),
("Découvrez Norvy en 30 minutes.","See Norvy in 30 minutes."),("Réserver une démonstration · norvy.lu","Book a demo · norvy.lu"),("Données hébergées en Europe · Migration offerte · Sans engagement","Data hosted in Europe · Free migration · No commitment")]
for a,b in T:
  if a not in s: print('MISSING',a[:50])
  s=s.replace(a,b)
s=s.replace('class="ref">UE-','class="ref">EU-').replace('class="ref">ONU-','class="ref">UN-')
open('film2-en.html','w',encoding='utf-8').write(s)
body=re.sub(r'<script.*?</script>','',s,flags=re.S)
print(set(re.findall(r'>[^<>]*[éèàùç][^<>]*<',body)))
