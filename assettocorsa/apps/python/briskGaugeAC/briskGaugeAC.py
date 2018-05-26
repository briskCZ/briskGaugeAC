##################################################
# briskGaugeAC
# 
# Version - 1.0.0
##################################################

import sys
import os
import platform
import ac
import acsys
import math

if platform.architecture()[0] == "64bit":
	sysdir = os.path.dirname(__file__)+'/thirdparty/stdlib64'
else:
	sysdir = os.path.dirname(__file__)+'/thirdparty/stdlib'

sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from thirdparty.sim_info import info

import ctypes

app_path = "apps/python/briskGaugeAC/"



is_valid = 1
this_lap = -1

def acMain(ac_version):
	global app_window
	global needle_path, rpm_gauge_path, speed_gauge_path, info_path, cluster_path
	global rpm_gauge_label, rpm_needle_label, speed_gauge_label, speed_needle_label, speed_label, speed_unit_label, rpm_label, rpm_unit_label
	global gear_label, clap_label, blap_label, plap_label, delta_label
	global flt_label, flp_label
	
	cluster_path = "textures/background/cluster"
	needle_path = "textures/needle/test_"
	
	ac.initFont(0, "Digital-7 Mono", 0, 0)
	#Font credit: Sizenko Alexander, Style-7, http://www.styleseven.com
	
	app_window = ac.newApp("briskGaugeAC")
	ac.setSize(app_window,600,240)
	ac.setIconPosition(app_window, 0, -10000)
	ac.setTitle(app_window, "")
	ac.drawBorder(app_window, 0)
	ac.setBackgroundTexture(app_window, app_path + cluster_path + ".png")
	ac.setBackgroundOpacity(app_window, 0.0)

	

	
	################### RPM STUFF
	rpm_gauge_path = "textures/background/rpm"

	rpm_gauge_label = ac.addLabel(app_window, "")
	ac.setSize(rpm_gauge_label, 240, 240)
	ac.setPosition(rpm_gauge_label, 0, 50)
	
	rpm_label = ac.addLabel(app_window,"")
	ac.setPosition(rpm_label, 78, 183)
	ac.setFontSize(rpm_label, 30)
	ac.setCustomFont(rpm_label, "Digital-7 Mono", 0, 0) 
	
	rpm_unit_label = ac.addLabel(app_window, "")
	ac.setPosition(rpm_unit_label, 140, 210)
	ac.setText(rpm_unit_label,"RPM")
	ac.setCustomFont(rpm_unit_label, "Digital-7 Mono", 0, 0) 
	
	rpm_needle_label = ac.addLabel(app_window, "")
	ac.setSize(rpm_needle_label, 220, 220)
	ac.setPosition(rpm_needle_label, 10, 60)
	###################
	
	################### SPEED STUFF
	speed_gauge_path = "textures/background/speed"
	
	speed_gauge_label = ac.addLabel(app_window, "")
	ac.setSize(speed_gauge_label, 240, 240)
	ac.setPosition(speed_gauge_label, 360, 50)
	
	speed_label = ac.addLabel(app_window,"")
	ac.setPosition(speed_label, 440, 183)
	ac.setFontSize(speed_label, 30)
	ac.setCustomFont(speed_label, "Digital-7 Mono", 0, 0) 
	
	speed_unit_label = ac.addLabel(app_window, "")
	ac.setPosition(speed_unit_label, 495, 210)
	ac.setText(speed_unit_label,"KM/H")
	ac.setCustomFont(speed_unit_label, "Digital-7 Mono", 0, 0) 
	
	speed_needle_label = ac.addLabel(app_window, "")
	ac.setSize(speed_needle_label, 220, 220)
	ac.setPosition(speed_needle_label, 370, 60)
	###################
	
	################### GEAR STUFF
	gear_label = ac.addLabel(app_window, "")
	ac.setPosition(gear_label, 285, 47)
	ac.setCustomFont(gear_label, "Digital-7 Mono", 0, 0) 
	ac.setFontSize(gear_label, 50)
	###################
	
	################### LAP TIMES
	clap_label = ac.addLabel(app_window, "")
	ac.setPosition(clap_label, 243, 207)
	ac.setCustomFont(clap_label, "Digital-7 Mono", 0, 0) 
	ac.setFontSize(clap_label, 17)
	
	blap_label = ac.addLabel(app_window, "")
	ac.setPosition(blap_label, 243, 167)
	ac.setCustomFont(blap_label, "Digital-7 Mono", 0, 0) 
	ac.setFontSize(blap_label, 17)
	
	plap_label = ac.addLabel(app_window, "")
	ac.setPosition(plap_label, 243, 187)
	ac.setCustomFont(plap_label, "Digital-7 Mono", 0, 0) 
	ac.setFontSize(plap_label, 17)
	
	delta_label = ac.addLabel(app_window, "")
	ac.setPosition(delta_label, 243, 147)
	ac.setCustomFont(delta_label, "Digital-7 Mono", 0, 0) 
	ac.setFontSize(delta_label, 17)
	###################

	return "briskGaugeAC"

def acUpdate(deltaT):
	global current_car, rpm, spin_rate, speed, lap_time, lap_sec, lap_min, gear, blap_time, blap_sec, blap_min, plap_time, plap_sec, plap_min, limiter, max_rpm, delta_time
	global is_valid, this_lap, laps
	ac.setBackgroundOpacity(app_window, 0.0)
	
	
	spin_rate_speed = 1.333
	
	max_rpm = info.static.maxRpm

	current_car = ac.getFocusedCar()
	
	limiter = ac.getCarState(0, acsys.CS.IsEngineLimiterOn) #zatim na nic
	
	################### RPM
	rpm = ac.getCarState(current_car, acsys.CS.RPM)
	
	if max_rpm <= 8000:
		spin_rate_rpm = 33.3
		ac.setBackgroundTexture(rpm_gauge_label, app_path + rpm_gauge_path + "8k.png")
	
	if max_rpm > 8000 and max_rpm < 10000:
		spin_rate_rpm = 41.625
		ac.setBackgroundTexture(rpm_gauge_label, app_path + rpm_gauge_path + "10k.png")
		
	if max_rpm > 10000 and max_rpm < 20000:
		spin_rate_rpm = 83.25
		ac.setBackgroundTexture(rpm_gauge_label, app_path + rpm_gauge_path + "20k.png")
	
	
	
	#ac.setBackgroundTexture(rpm_needle_label, app_path + needle_path + "{:.0f}".format(rpm / spin_rate_rpm).zfill(3) + ".png")
	ac.setBackgroundTexture(rpm_needle_label, app_path + needle_path + "{:.0f}".format(rpm / spin_rate_rpm) + ".png")
	ac.setText(rpm_label,"{:.0f}".format(rpm))
	
	################### SPEED
	speed = ac.getCarState(current_car, acsys.CS.SpeedKMH)

	ac.setBackgroundTexture(speed_gauge_label, app_path + speed_gauge_path + ".png")
	#ac.setBackgroundTexture(speed_needle_label, app_path + needle_path + "{:.0f}".format(speed / spin_rate_speed).zfill(3) + ".png")
	ac.setBackgroundTexture(speed_needle_label, app_path + needle_path + "{:.0f}".format(speed / spin_rate_speed)+ ".png")
	ac.setText(speed_label,"{:.0f}".format(speed))
	
	###################LAPTIMES
	lap_time = ac.getCarState(0, acsys.CS.LapTime)
	lap_sec = (lap_time / 1000) % 60
	lap_min = (lap_time // 1000) // 60
	ac.setText(clap_label,"CURR: " +"{:.0f}:{:06.3f}".format(lap_min,lap_sec))
	
	blap_time = ac.getCarState(0, acsys.CS.BestLap)
	blap_sec = (blap_time / 1000) % 60
	blap_min = (blap_time // 1000) // 60
	ac.setText(blap_label,"BEST: " +"{:.0f}:{:06.3f}".format(blap_min,blap_sec))
	
	plap_time = ac.getCarState(0, acsys.CS.LastLap)
	plap_sec = (plap_time / 1000) % 60
	plap_min = (plap_time // 1000) // 60
	ac.setText(plap_label,"PREV: " +"{:.0f}:{:06.3f}".format(plap_min,plap_sec))
	
	delta_time = ac.getCarState(0, acsys.CS.PerformanceMeter)
	ac.setText(delta_label,"DELT: " +"{:+.3f}".format(delta_time))
	if delta_time > 0:
		ac.setFontColor(delta_label, 1, 0.17, 0, 1)#red
	if delta_time == 0:
		ac.setFontColor(delta_label, 1, 1, 1, 1)#white
	if delta_time < 0:
		ac.setFontColor(delta_label, 0, 0.780, 0.145, 1)#green
	
	laps = ac.getCarState(0, acsys.CS.LapCount)
	
	if info.physics.numberOfTyresOut > 2:
		is_valid = 0
		this_lap = laps
	
	if this_lap == laps:	
		if is_valid == 0:
			ac.setFontColor(clap_label, 1, 0.17, 0, 1)#cervena
		elif is_valid == 1:
			ac.setFontColor(clap_label, 1, 1, 1, 1)#bila
	if this_lap != laps:
		is_valid = 1
		ac.setFontColor(clap_label, 1, 1, 1, 1)#bila
	
	###################GEARS
	gear = ac.getCarState(0, acsys.CS.Gear)
	if gear == 0: 
		ac.setText(gear_label,"R")
	elif gear == 1: 
		ac.setText(gear_label,"N")
	else: 
		ac.setText(gear_label,"{}".format(gear - 1))
		
	if rpm >= max_rpm - 300:
		ac.setFontColor(gear_label, 1, 0.17, 0, 1)#red
	else:
		ac.setFontColor(gear_label, 1, 1, 1, 1)#white