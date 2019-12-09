import os
import my_decrypt
import time
import datetime

pdf_24hr_adm_sum = "http://147.32.80.119:5621/api/reporting/generate/printablePdf?jobParams=(browserTimezone:Europe%2FBratislava,layout:(dimensions:(height:1687.98828125,width:1557.01171875),id:preserve_layout),objectType:dashboard,relativeUrls:!(%27%2Fapp%2Fkibana%23%2Fdashboard%2F5d9f1e80-ca59-11e9-99e4-650811b1eba3%3F_g%3D(refreshInterval:(pause:!!t,value:0),time:(from:now-24h,to:now))%26_a%3D(description:!%27Most%2Bimportant%2Binformation!%27,filters:!!(),fullScreenMode:!!f,options:(hidePanelTitles:!!f,useMargins:!!t),panels:!!((embeddableConfig:(),gridData:(h:9,i:!%273!%27,w:23,x:25,y:0),id:eb959d50-be9b-11e9-99e4-650811b1eba3,panelIndex:!%273!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:9,i:!%274!%27,w:25,x:0,y:0),id:fc86bc90-8294-11e9-9558-a1ced9d4dc76,panelIndex:!%274!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:10,i:!%275!%27,w:48,x:0,y:50),id:ae2fd720-be76-11e9-99e4-650811b1eba3,panelIndex:!%275!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:10,i:!%277!%27,w:48,x:0,y:31),id:b523d340-8296-11e9-9558-a1ced9d4dc76,panelIndex:!%277!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:10,i:!%278!%27,w:48,x:0,y:21),id:!%271cdef600-9c0e-11e9-8bd7-cf34fb361974!%27,panelIndex:!%278!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%279!%27,w:22,x:0,y:9),id:!%2779cc0b30-ca5f-11e9-99e4-650811b1eba3!%27,panelIndex:!%279!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:9,i:!%2710!%27,w:48,x:0,y:41),id:!%2723a5b2e0-b85a-11e9-9b9c-0b2ee2fa0098!%27,panelIndex:!%2710!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%2712!%27,w:16,x:32,y:9),id:!%275f83d070-f01e-11e9-90fc-7f3071ab5b4d!%27,panelIndex:!%2712!%27,title:!%27Total%2BCount%2Bof%2BRouters%2Bover%2BTime!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%2713!%27,w:10,x:22,y:9),id:c1b021d0-c40f-11e9-99e4-650811b1eba3,panelIndex:!%2713!%27,type:visualization,version:!%277.0.1!%27)),query:(language:kuery,query:!%27!%27),timeRestore:!!f,title:Summary,viewMode:view)%27),title:Summary)"
pdf_24hr_adm_ips = "http://147.32.80.119:5621/api/reporting/generate/printablePdf?jobParams=(browserTimezone:Europe%2FBratislava,layout:(dimensions:(height:3591.9921875,width:1557.01171875),id:preserve_layout),objectType:dashboard,relativeUrls:!(%27%2Fapp%2Fkibana%23%2Fdashboard%2Fe2f413f0-9cd3-11e9-874b-3da6c4262ccd%3F_g%3D(refreshInterval:(pause:!!t,value:0),time:(from:now-24h,to:now))%26_a%3D(description:!%27Source%2Bcountries%2Bof%2Bdata%2Bflows!%27,filters:!!(),fullScreenMode:!!f,options:(hidePanelTitles:!!f,useMargins:!!t),panels:!!((embeddableConfig:(),gridData:(h:38,i:!%271!%27,w:17,x:0,y:11),id:!%2703e4b230-9271-11e9-81c1-799846d8268f!%27,panelIndex:!%271!%27,title:!%27Total%2BPackets%2Bfrom%2BIP%2Bto%2BDestination%2BPort!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%273!%27,w:15,x:33,y:11),id:!%275f454e20-98b9-11e9-8295-79fa7efdb491!%27,panelIndex:!%273!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(mapCenter:!!(17.978733095556183,8.789062500000002),mapZoom:2),gridData:(h:15,i:!%277!%27,w:48,x:0,y:49),id:b82d4ce0-824d-11e9-964e-b9b787c6d780,panelIndex:!%277!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:13,i:!%2715!%27,w:15,x:33,y:23),id:!%275d09c5a0-9ca1-11e9-8bd7-cf34fb361974!%27,panelIndex:!%2715!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%2716!%27,w:16,x:17,y:11),id:d2202320-9ca1-11e9-8bd7-cf34fb361974,panelIndex:!%2716!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:34,i:!%2726!%27,w:24,x:24,y:79),id:!%272c01e260-9cb7-11e9-8bd7-cf34fb361974!%27,panelIndex:!%2726!%27,title:!%27Total%2BPackets%2Bfrom%2BIP%2Baddress%2Bto%2BRouter%2BID!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:11,i:!%2727!%27,w:35,x:0,y:0),id:!%27424f8be0-9cd4-11e9-874b-3da6c4262ccd!%27,panelIndex:!%2727!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:11,i:!%2728!%27,w:13,x:35,y:0),id:!%270107b900-bcfa-11e9-9b9c-0b2ee2fa0098!%27,panelIndex:!%2728!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:7,i:!%2729!%27,w:48,x:0,y:113),id:f5db81e0-be77-11e9-99e4-650811b1eba3,panelIndex:!%2729!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(vis:(params:(sort:(columnIndex:3,direction:desc)))),gridData:(h:19,i:!%2730!%27,w:24,x:0,y:79),id:!%2704f92fd0-bead-11e9-99e4-650811b1eba3!%27,panelIndex:!%2730!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:15,i:!%2731!%27,w:24,x:0,y:98),id:cd2ab3d0-eff3-11e9-90fc-7f3071ab5b4d,panelIndex:!%2731!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:8,i:!%2732!%27,w:48,x:0,y:120),id:fc86bc90-8294-11e9-9558-a1ced9d4dc76,panelIndex:!%2732!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(mapCenter:!!(17.644022027872726,5.800781250000001),mapZoom:2),gridData:(h:15,i:!%2733!%27,w:48,x:0,y:64),id:!%275c1d20a0-f030-11e9-90fc-7f3071ab5b4d!%27,panelIndex:!%2733!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:13,i:!%2734!%27,w:16,x:17,y:36),id:ef931100-f030-11e9-90fc-7f3071ab5b4d,panelIndex:!%2734!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:13,i:!%2735!%27,w:15,x:33,y:36),id:!%2737dc50c0-f031-11e9-90fc-7f3071ab5b4d!%27,panelIndex:!%2735!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:6,i:!%2736!%27,w:16,x:17,y:23),id:cf066f80-f031-11e9-90fc-7f3071ab5b4d,panelIndex:!%2736!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:7,i:!%2737!%27,w:16,x:17,y:29),id:!%271b5d6f50-f032-11e9-90fc-7f3071ab5b4d!%27,panelIndex:!%2737!%27,type:visualization,version:!%277.0.1!%27)),query:(language:kuery,query:!%27!%27),timeRestore:!!f,title:!%27IP%2BAddresses!%27,viewMode:view)%27),title:%27IP%20Addresses%27)"

png_24hr_adm_sum = 'http://147.32.80.119:5621/api/reporting/generate/png?jobParams=(browserTimezone:Europe%2FBratislava,layout:(dimensions:(height:1687.98828125,width:1557.01171875),id:png),objectType:dashboard,relativeUrl:%27%2Fapp%2Fkibana%23%2Fdashboard%2F5d9f1e80-ca59-11e9-99e4-650811b1eba3%3F_g%3D(refreshInterval:(pause:!!t,value:0),time:(from:now-24h,to:now))%26_a%3D(description:!%27Most%2Bimportant%2Binformation!%27,filters:!!(),fullScreenMode:!!f,options:(hidePanelTitles:!!f,useMargins:!!t),panels:!!((embeddableConfig:(),gridData:(h:9,i:!%273!%27,w:23,x:25,y:0),id:eb959d50-be9b-11e9-99e4-650811b1eba3,panelIndex:!%273!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:9,i:!%274!%27,w:25,x:0,y:0),id:fc86bc90-8294-11e9-9558-a1ced9d4dc76,panelIndex:!%274!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:10,i:!%275!%27,w:48,x:0,y:50),id:ae2fd720-be76-11e9-99e4-650811b1eba3,panelIndex:!%275!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:10,i:!%277!%27,w:48,x:0,y:31),id:b523d340-8296-11e9-9558-a1ced9d4dc76,panelIndex:!%277!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:10,i:!%278!%27,w:48,x:0,y:21),id:!%271cdef600-9c0e-11e9-8bd7-cf34fb361974!%27,panelIndex:!%278!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%279!%27,w:22,x:0,y:9),id:!%2779cc0b30-ca5f-11e9-99e4-650811b1eba3!%27,panelIndex:!%279!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:9,i:!%2710!%27,w:48,x:0,y:41),id:!%2723a5b2e0-b85a-11e9-9b9c-0b2ee2fa0098!%27,panelIndex:!%2710!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%2712!%27,w:16,x:32,y:9),id:!%275f83d070-f01e-11e9-90fc-7f3071ab5b4d!%27,panelIndex:!%2712!%27,title:!%27Total%2BCount%2Bof%2BRouters%2Bover%2BTime!%27,type:visualization,version:!%277.0.1!%27),(embeddableConfig:(),gridData:(h:12,i:!%2713!%27,w:10,x:22,y:9),id:c1b021d0-c40f-11e9-99e4-650811b1eba3,panelIndex:!%2713!%27,type:visualization,version:!%277.0.1!%27)),query:(language:kuery,query:!%27!%27),timeRestore:!!f,title:Summary,viewMode:view)%27,title:Summary)'

#pdf_24hr_adm_rou = 
#pdf_24hr_adm_ale =
#pdf_24hr_adm_req = 
#pdf_24hr_adm_rsp =
#pdf_24hr_adm_met = 


 
if __name__ == '__main__':
    fin = "/home/kalin/str/.stuff/"
    fcreds = ['.elastic']
    decrypted = my_decrypt.decrypt(fin, fcreds)
    
    cmd_sum = "curl -X POST -H 'kbn-version: 7.0.1' '{}' -u elastic:'{}'".format(pdf_24hr_adm_sum, decrypted[0])
    cmd_ips = "curl -X POST -H 'kbn-version: 7.0.1' '{}' -u elastic:'{}'".format(pdf_24hr_adm_ips, decrypted[0])
    while(True):
        print("Generating Report...")
        rsp_sum = os.popen(cmd_sum).read()
        
        start = rsp_sum.find('/download/') + 10
        rsp_sum = rsp_sum[start:-1]
        end = rsp_sum.find('\"')
        fname = "Summary_" + str(datetime.datetime.now()).split('.')[0]+'.pdf'
        fname = fname.replace(' ', '_')
        fout = rsp_sum[0:end]
        time.sleep(60*1)
        print("Saving Report: {}".format(fname))
        print(fout)
        try:
            cmd = "curl http://147.32.80.119:5621/api/reporting/jobs/download/{} --output '/home/kalin/str/reports/{}' -u elastic:'{}'".format(fout, fname, decrypted[0])
            os.system(cmd)
        except Exception as e:
            print(e)
        
        report2slack = """curl -F file=@/home/kalin/str/reports/{} -F "initial_comment=Summary Dashboard for last 24 hours" -F channels=DGQA89H19 -F "username=Ludus Notifier" -F "emoji=ludus" -H "Authorization: autorization" https://slack.com/api/files.upload""".format(fname)
        os.system(report2slack)
        
#        rsp_ips = os.system(cmd_ips)
#        time.sleep(60*8)
        print("Sleeping for 24 hrs")
        time.sleep(60*60*24-60*8*2-1)
        
    

