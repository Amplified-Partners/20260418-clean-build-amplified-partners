CIS Google Chrome  Enterprise Core Browser  Benchmark 

v1.0.0 \- 06-30-2025

Internal Only \- General   
**Terms of Use** 

Please see the below link for our current terms of use: 

https://www.cisecurity.org/cis-securesuite/cis-securesuite-membership-terms-of-use/ 

For information on referencing and/or citing CIS Benchmarks in 3rd party documentation  (including using portions of Benchmark Recommendations) please contact CIS Legal  (legalnotices@cisecurity.org) and request guidance on copyright usage.  

**NOTE**: It is ***NEVER*** acceptable to host a CIS Benchmark in ***ANY*** format (PDF, etc.)  on a 3rd party (non-CIS owned) site.

Page 1 

Internal Only \- General   
**Table of Contents** 

***Terms of Use..................................................................................................................... 1 Table of Contents ............................................................................................................. 2 Overview............................................................................................................................ 8*** 

**Important Usage Information.................................................................................................... 8 Key Stakeholders....................................................................................................................................8 Apply the Correct Version of a Benchmark.........................................................................................9 Exceptions...............................................................................................................................................9 Remediation ..........................................................................................................................................10 Summary................................................................................................................................................10** 

**Target Technology Details ...................................................................................................... 11 Intended Audience ................................................................................................................... 11 Consensus Guidance............................................................................................................... 12 Typographical Conventions.................................................................................................... 13** 

***Recommendation Definitions ....................................................................................... 14*** **Title............................................................................................................................................. 14** 

**Assessment Status .................................................................................................................. 14 Automated .............................................................................................................................................14 Manual....................................................................................................................................................14** 

**Profile......................................................................................................................................... 14 Description................................................................................................................................ 14 Rationale Statement................................................................................................................. 14 Impact Statement...................................................................................................................... 15 Audit Procedure........................................................................................................................ 15 Remediation Procedure........................................................................................................... 15 Default Value............................................................................................................................. 15 References ................................................................................................................................ 15 CIS Critical Security Controls®(CIS Controls®).................................................................... 15 Additional Information............................................................................................................. 15 Profile Definitions..................................................................................................................... 16 Acknowledgements.................................................................................................................. 17** 

***Recommendations ......................................................................................................... 18*** 

**1 Introduction............................................................................................................................ 18** Recommendation Order..........................................................................................................18 Enforced Defaults....................................................................................................................18 Viewing the Resulting "Policies" in Chrome............................................................................18 

**2 Settings................................................................................................................................... 19**

Page 2 

Internal Only \- General   
**2.1 Sign-in Settings ..............................................................................................................................20** 2.1.1 (L2) Ensure 'Browser sign in settings' is set to 'Disabled browser sign-in' (Automated) .21 2.1.2 (L1) Ensure 'Azure Cloud Authentication' Is Set to 'Enable Azure cloud authentication'  (Manual).....................................................................................................................................23 

**2.2 Apps and Extensions.....................................................................................................................25** 2.2.1 (L2) Ensure 'Manifest v2 extension availability' Is Set to 'Enable force-installed manifest  v2 extensions on the sign-in screen' (Automated) ....................................................................26 

**2.3 Site Isolation ...................................................................................................................................28** 2.3.1 (L1) Ensure 'Site isolation' is set to 'Require Site Isolation for all websites, as well as any  origins below' (Automated) ........................................................................................................29 

**2.4 Security............................................................................................................................................31** 2.4.1 (L1) Ensure 'Password manager' is Explicitly Configured (Manual) ................................32 2.4.2 (L1) Ensure 'Web Authentication requests on sites with broken TLS certificates' Is Set to  'Do not allow WebAuthn API requests on sites with broken TLS certificates' (Automated)......34 2.4.3 (L1) Ensure 'Post-quantum TLS' Is Set to 'Allow post-quantum key agreement in TLS  

connections' (Automated)..........................................................................................................36 2.4.4 (L1) Ensure 'Incognito mode' is set to 'Disallow incognito mode' (Automated) ...............38 2.4.5 (L1) Ensure 'Browser history' is set to 'Always save browser history' (Automated).........40 2.4.6 (L1) Ensure 'Clear browser history' Is Set to 'Do not allow clearing history in settings  

menu' (Automated) ....................................................................................................................42 2.4.7 (L1) Ensure 'Force ephemeral mode' is set to 'Do not erase local user data' (Automated) ...................................................................................................................................................44 2.4.8 (L1) Ensure 'Online revocation checks' is set to 'Perform online OCSP/CRL checks'  (Automated)...............................................................................................................................46 2.4.9 (L1) Ensure 'Geolocation' is set to 'Do not allow sites to detect users' geolocation'  (Automated)...............................................................................................................................48 2.4.10 (L1) Ensure 'Allowed certificate transparency URLs' is Not Set (Automated) ...............50 2.4.11 (L1) Ensure 'Certificate transparency CA allowlist' is Not Set (Automated) ..................52 2.4.12 (L1) Ensure 'Renderer App Container' Is Set to 'Enable the Renderer App Container  sandbox' (Automated)................................................................................................................54 2.4.13 (L1) Ensure 'Enable leak detection for entered credentials' Is Set to 'Enable Leak  detection for entered credentials' (Manual)...............................................................................56 2.4.14 (L1) Ensure 'Audio sandbox' is set to 'Always sandbox the audio process' (Automated) ...................................................................................................................................................58 2.4.15 (L1) Ensure 'Unsupported system warning' is set to 'Allow Chrome to display warnings  when running on an unsupported system' (Automated)............................................................60 2.4.16 (L2) Ensure 'Advanced Protection program' Is Set to 'Users enrolled in the Advanced  Protection program will receive extra protections' (Manual) .....................................................62 2.4.17 (L1) Ensure 'Override insecure origin restrictions' is Not Set (Automated) ...................64 2.4.18 (L1) Ensure 'Command-line flags' is set to 'Show security warnings when potentially  dangerous command-line flags are used' (Automated) ............................................................66 2.4.19 (L1) Ensure 'Allow remote debugging' is set to 'Do not allow use of the remote  debugging' (Automated) ............................................................................................................68 2.4.20 (L1) Ensure 'TLS encrypted ClientHello' Is 'Enable the TLS Encrypted ClientHello  experiment' (Automated) ...........................................................................................................70 2.4.21 (L1) Ensure 'Strict MIME type checking for worker scripts' Is Set to 'Require a  JavaScript MIME type for worker scripts' (Automated) .............................................................72 2.4.22 (L2) Ensure 'Enforce local anchor constraints' Is 'Enforce constraints in locally added  trust anchors' (Automated) ........................................................................................................74 2.4.23 (L1) Ensure 'File/directory picker without user gesture' Is Not Set (Automated) ...........76 2.4.24 (L1) Ensure 'Media picker without user gesture' Is Not Configured (Automated)..........78 

**2.5 Remote access (Chrome Remote Desktop).................................................................................80** 2.5.1 (L1) Ensure 'Remote access hosts' is set with a domain defined in 'Remote access host  domain' (Manual).......................................................................................................................81 2.5.2 (L1) Ensure 'Firewall traversal' is set to 'Disable firewall traversal' (Automated).............83 2.5.3 (L1) Ensure 'Firewall traversal' is set to 'Disable the use of relay servers' (Automated) .85

Page 3 

Internal Only \- General   
2.5.4 (L1) Ensure 'Remote support connections' is set to 'Prevent remote support connections'  (Manual).....................................................................................................................................87 **2.6 Network............................................................................................................................................89** 2.6.1 (L1) Ensure 'Proxy mode' is Not Set to 'Always auto detect the proxy' (Automated) ......90 

2.6.2 (L2) Ensure 'Supported authentication schemes' is set to 'NTLM' and 'Negotiate'  (Automated)...............................................................................................................................92 2.6.3 (L2) Ensure 'SSL error override' is set to 'Block users from clicking through SSL  warnings' (Automated)...............................................................................................................94 2.6.4 (L1) Ensure 'WebRTC ICE candidate URLs for local IPs' Is Not Set (Automated)..........96 2.6.5 (L2) Ensure 'DNS over HTTPS' is set to 'Enable DNS-over-HTTPS without insecure  fallback' (Automated).................................................................................................................98 2.6.6 (L1) Ensure 'Cross-origin authentication' is set to 'Block cross-origin authentication'  (Automated).............................................................................................................................101 2.6.7 (L1) Ensure 'Enable globally scoped HTTP authentication cache' is set to 'Disabled'  (Automated).............................................................................................................................103 2.6.8 (L1) Ensure 'HSTS policy bypass list' is Not Set (Automated).......................................105 2.6.9 (L1) Ensure 'DNS interception checks enabled' is set to 'Perform DNS interception  checks ' (Automated)...............................................................................................................107 2.6.10 (L1) Ensure 'Network service sandbox' Is Set to 'Enable the network sandbox'  (Automated).............................................................................................................................109 2.6.11 (L1) Ensure 'Http Allowlist' Is Properly Configured (Manual) .......................................111 2.6.12 (L1) Ensure 'Automatic HTTPS upgrades' Is Set to 'Allow HTTPS upgrades'  (Automated).............................................................................................................................113 

**2.7 Import Settings .............................................................................................................................115** 2.7.1 (L1) Ensure 'Import autofill data' is set to 'Disable imports of autofill data' (Automated) .................................................................................................................................................116 2.7.2 (L1) Ensure 'Import homepage' is set to 'Disable imports of homepage' (Automated)..118 2.7.3 (L1) Ensure 'Import saved passwords' is set to 'Disable imports of saved passwords'  (Automated).............................................................................................................................120 2.7.4 (L1) Ensure 'Import search engines' is set to 'Disable imports of search engines'  (Automated).............................................................................................................................122 

**2.8 Content ..........................................................................................................................................124** 2.8.1 (L2) Ensure 'Screen video capture' is set to 'Do not allow sites to prompt the user to  share a video stream of their screen' (Automated) .................................................................125 2.8.2 (L1) Ensure 'Cast' is set to 'Do not allow users to cast' (Automated) ............................127 2.8.3 (L1) Ensure 'Clipboard' Is Set to 'Do not allow any site to use the clipboard site  permission' (Automated)..........................................................................................................129 2.8.4 (L1) Ensure 'Enable URL-keyed anonymized data collection' is set to 'Data collection is  never active' (Automated)........................................................................................................132 2.8.5 (L1) Ensure 'Third-party cookie blocking' is set to 'Disallow third-party cookies'  (Automated).............................................................................................................................134 2.8.6 (L1) Ensure 'Cast' is set to 'Do not allow users to Cast' (Automated)............................136 2.8.7 (L2) Ensure 'Cookies' is set to 'Session Only' (Automated) ...........................................138 2.8.8 (L2) Ensure 'SafeSearch and Restricted Mode' is set to 'Always use Safe Search for  Google Web Search queries' (Automated)..............................................................................140 2.8.9 (L1) Ensure 'First-Party Sets' Is Set to 'Disable First-Party Sets for all affected users'  (Manual)...................................................................................................................................142 2.8.10 (L1) Ensure 'Allow local file access to file:// URLs on these sites in the PDF Viewer' Is  Not Set (Automated)................................................................................................................144 2.8.11 (L2) Ensure 'Notifications' is set to 'Do not allow any site to show desktop notifications'  (Automated).............................................................................................................................146 2.8.12 (L2) Ensure 'WebUSB API' is set to 'Do not allow any site to request access to USB  devices via the WebUSB API' (Automated) ............................................................................148 2.8.13 (L1) Ensure 'Allow third-party partitioning to be enabled' in 'Third-party storage  partitioning' Is Configured (Manual).........................................................................................150

Page 4 

Internal Only \- General   
2.8.14 (L2) Ensure 'Third-party storage partitioning' Is Set to 'Block third-party storage  partitioning from being enabled' (Automated) .........................................................................152 2.8.15 (L2) Ensure 'Web Bluetooth API' is set to 'Do not allow any site to request access to  Bluetooth devices via the Web Bluetooth API' (Automated) ...................................................154 2.8.16 (L1) Ensure 'Control use of insecure content exceptions' is set to 'Do not allow any site  to load mixed content' (Automated).........................................................................................156 

**2.9 User Experience............................................................................................................................158** 2.9.1 (L1) Ensure 'Download location prompt' is set to 'Ask the user where to save the file  before downloading' (Automated)............................................................................................159 2.9.2 (L2) Ensure 'Browser guest mode' is set to 'Prevent guest browser logins' (Automated) .................................................................................................................................................161 2.9.3 (L1) Ensure 'Credit card form Autofill' is set to 'Never Autofill credit card forms'  (Automated).............................................................................................................................163 2.9.4 (L2) Ensure 'Address form Autofill' is set to 'Never Autofill address forms' (Automated) .................................................................................................................................................165 2.9.5 (L1) Ensure 'Allow user feedback' is set to 'Do not allow user feedback' (Automated) .167 2.9.6 (L2) Ensure 'File selection dialogs' is set to 'Block file selection dialogs' (Automated) .169 2.9.7 (L2) Ensure 'Google Translate' is set to 'Never offer translation' (Automated)..............171 2.9.8 (L1) Ensure 'Spell check service' is set to 'Disable the spell checking web service'  (Automated).............................................................................................................................173 2.9.9 (L1) Ensure 'Network prediction' Is Set to 'Do not predict network actions' (Automated) .................................................................................................................................................175 2.9.10 (L1) Ensure 'Alternate error pages' is set to 'Never use alternate error pages'  (Automated).............................................................................................................................177 2.9.11 (L1) Ensure 'Payment methods' is set to 'Always tell websites that no payment methods  are saved' (Automated) ...........................................................................................................179 

**2.10 Omnibox Search Provider .........................................................................................................181** 2.10.1 (L2) Ensure 'Search suggest' is set to 'Never allow users to use Search Suggest'  (Automated).............................................................................................................................182 2.10.2 (L1) Ensure 'Side Panel search' Is Set to 'Disable Side Panel search on all web pages'  (Automated).............................................................................................................................184 

**2.11 Hardware .....................................................................................................................................186** 2.11.1 (L1) Ensure 'Enterprise Hardware Platform API' is set to 'Do not allow managed  extensions to use the Enterprise Hardware Platform API' (Automated) .................................187 2.11.2 (L2) Ensure 'Video input (camera)' is set to 'Disable camera input for websites and  apps' (Automated) ...................................................................................................................189 2.11.3 (L2) Ensure 'Audio input (microphone)' is set to 'Disable audio input' (Automated) ....191 2.11.4 (L2) Ensure 'Sensors' is set to 'Do not allow any site to access sensors' (Automated) .................................................................................................................................................193 2.11.5 (L2) Ensure 'Web Serial API' is set to 'Do not allow any site to request access to serial  ports via the Web Serial API' (Automated)..............................................................................195 

**2.12 Chrome Safe Browsing..............................................................................................................197** 2.12.1 (L1) Ensure no URLs Are Configured in 'Safe Browsing allowed domains' (Automated) .................................................................................................................................................198 2.12.2 (L1) Ensure 'Safe Browsing for trusted sources' is set to 'Perform Safe Browsing  checks on all downloaded files' (Automated) ..........................................................................200 2.12.3 (L1) Ensure 'Disable bypassing Safe Browsing warnings' is set to 'Do not allow user to  bypass Safe Browsing warning' (Automated)..........................................................................202 2.12.4 (L1) Ensure 'Download restrictions' is set to 'Block malicious downloads' (Automated) .................................................................................................................................................204 2.12.5 (L1) Ensure 'Suppress lookalike domain warnings on domains' is Not Set (Automated) .................................................................................................................................................206 2.12.6 (L2) Ensure 'SafeSites URL filter' is set to 'Filter top level sites (but not embedded  iframes) for adult content' (Automated) ...................................................................................209 2.12.7 (L1) Ensure 'Safe Browsing protection' is set to 'Safe Browsing is active in the standard  mode' and 'Allow higher-protection proxied lookups' (Manual)...............................................211

Page 5 

Internal Only \- General   
**2.13 Generative AI...............................................................................................................................214** 2.13.1 Ensure 'Generative AI policy defaults' Is Set to 'Allow GenAI features without improving  AI models' (Automated) ...........................................................................................................215 2.13.2 Ensure 'Help me write' Is Set to 'Use the value specified in the Generative AI policy  

defaults setting' (Automated)...................................................................................................217 2.13.3 Ensure 'DevTools AI features' Is Set to 'Use the value specified in the Generative AI  policy defaults setting' (Automated).........................................................................................219 2.13.4 Ensure 'History search settings' Is Set to 'Use the value specified in the Generative AI  policy defaults setting' (Automated).........................................................................................221 2.13.5 Ensure 'Tab compare' Is Set to 'Use the value specified in the Generative AI policy  defaults setting' (Automated)...................................................................................................223 2.13.6 Ensure 'Help me read' Is Set to 'Use the value specified in the Generative AI policy  defaults setting' (Manual) ........................................................................................................225 

**2.14 Chrome Updates.........................................................................................................................226** 2.14.1 (L1) Ensure 'Component updates' is set to 'Enable updates for all components'  (Automated).............................................................................................................................227 2.14.2 (L1) Ensure 'Relaunch notification' sets 'Time Period (hours)' to '168 or less' and 'Initial  quiet period (hours)' to less than 'Time Period (hours)' (Automated)......................................230 2.14.3 (L1) Ensure 'Relaunch notification' is set to 'Show notification recommending relaunch'  (Automated).............................................................................................................................232 

**2.15 Chrome Variations......................................................................................................................234** 2.15.1 (L1) Ensure 'Variations' is set to 'Enable Chrome variations' (Manual) .......................235 **2.16 Other Settings.............................................................................................................................238** 

2.16.1 (L1) Ensure 'Google time service' is set to 'Allow queries to a Google server to retrieve  an accurate timestamp' (Automated).......................................................................................239 2.16.2 (L1) Ensure 'Disk cache size in bytes' in 'Disk cache size' is set to \`250609664'  (Automated).............................................................................................................................242 2.16.3 (L1) Ensure 'Chrome Sync (ChromeOS)' is set to 'Allow Chrome Sync' and Exclude  'Passwords' (Automated).........................................................................................................244 2.16.4 (L1) Ensure 'Metrics reporting' is set to 'Do not send anonymous reports of usage and  crash-related data to Google' (Automated) .............................................................................246 2.16.5 (L1) Ensure 'Chrome Sync and Roaming Profiles (Chrome Browser \- Cloud Managed)'  is set to 'Disallow Sync' (Automated) ......................................................................................248 2.16.6 (L1) Ensure 'Allow reporting of domain reliability related data' Is 'Never send domain  reliability data to Google' (Automated) ....................................................................................250 2.16.7 (L2) Ensure 'Prohibited Native Messaging hosts' in 'Native Messaging blocked hosts' is  set to '\*' (Automated) ...............................................................................................................252 2.16.8 (L1) Ensure 'Background mode' is set to 'Disable background mode' (Automated)....254 

**3 Apps & Extensions.............................................................................................................. 256 3.1 Extensions.....................................................................................................................................257** 3.1.1 (L1) Ensure 'External extensions' is set to 'Block external extensions from being  installed' (Automated)..............................................................................................................258 3.1.2 (L1) Ensure 'Allowed types of apps and extensions' is set to 'Extension', 'Hosted App',  'Chrome Packaged App', and 'Theme' (Automated) ...............................................................260 3.1.3 (L1) Ensure 'App and extension install sources' Is Not Set (Automated) ......................262 3.1.4 (L1) Ensure 'Chrome Web Store unpublished extensions' Is Set to 'Disable unpublished  extensions' (Automated)..........................................................................................................264 

***Appendix: Summary Table.......................................................................................... 266 Appendix: CIS Controls v7 IG 1 Mapped Recommendations................................. 276 Appendix: CIS Controls v7 IG 2 Mapped Recommendations................................. 278 Appendix: CIS Controls v7 IG 3 Mapped Recommendations................................. 284 Appendix: CIS Controls v7 Unmapped Recommendations.................................... 290***

Page 6 

Internal Only \- General   
***Appendix: CIS Controls v8 IG 1 Mapped Recommendations................................. 291 Appendix: CIS Controls v8 IG 2 Mapped Recommendations................................. 295 Appendix: CIS Controls v8 IG 3 Mapped Recommendations................................. 301 Appendix: CIS Controls v8 Unmapped Recommendations.................................... 307 Appendix: Change History .......................................................................................... 308***

Page 7 

Internal Only \- General   
**Overview** 

All CIS Benchmarks™ (Benchmarks) focus on technical configuration settings used to  maintain and/or increase the security of the addressed technology, and they should be  used in **conjunction** with other essential cyber hygiene tasks like: 

• Monitoring the base operating system and applications for vulnerabilities and  quickly updating with the latest security patches. 

• End-point protection (Antivirus software, Endpoint Detection and Response  (EDR), etc.). 

• Logging and monitoring user and system activity. 

In the end, the Benchmarks are designed to be a key **component** of a comprehensive  cybersecurity program.  

**Important Usage Information** 

All Benchmarks are available free for non-commercial use from the CIS Website. They  can be used to manually assess and remediate systems and applications. In lieu of  manual assessment and remediation, there are several tools available to assist with  assessment: 

• CIS Configuration Assessment Tool (CIS-CAT® Pro Assessor) 

• CIS Benchmarks™ Certified 3rd Party Tooling 

These tools make the hardening process much more scalable for large numbers of  systems and applications.  

**NOTE**: Some tooling focuses only on the Benchmark Recommendations that can  be fully automated (skipping ones marked **Manual**). It is important that ***ALL*** Recommendations (**Automated** and **Manual**) be addressed since all are  important for properly securing systems and are typically in scope for  audits.  

**Key Stakeholders** 

Cybersecurity is a collaborative effort, and cross functional cooperation is imperative  within an organization to discuss, test, and deploy Benchmarks in an effective and  efficient way. The Benchmarks are developed to be best practice configuration  guidelines applicable to a wide range of use cases. In some organizations, exceptions  to specific Recommendations will be needed, and this team should work to prioritize the  problematic Recommendations based on several factors like risk, time, cost, and labor.  These exceptions should be properly categorized and documented for auditing  purposes.

Page 8 

Internal Only \- General   
**Apply the Correct Version of a Benchmark** 

Benchmarks are developed and tested for a specific set of products and versions and  applying an incorrect Benchmark to a system can cause the resulting pass/fail score to  be incorrect. This is due to the assessment of settings that do not apply to the target  systems. To assure the correct Benchmark is being assessed:  

• **Deploy the Benchmark applicable to the way settings are managed in the  environment:** An example of this is the Microsoft Windows family of  Benchmarks, which have separate Benchmarks for Group Policy, Intune, and  Stand-alone systems based upon how system management is deployed.  Applying the wrong Benchmark in this case will give invalid results. 

• **Use the most recent version of a Benchmark**: This is true for all Benchmarks,  but especially true for cloud technologies. Cloud technologies change frequently  and using an older version of a Benchmark may have invalid methods for  auditing and remediation. 

**Exceptions** 

The guidance items in the Benchmarks are called recommendations and not  requirements, and exceptions to some of them are expected and acceptable. The  Benchmarks strive to be a secure baseline, or starting point, for a specific technology,  with known issues identified during Benchmark development are documented in the  Impact section of each Recommendation. In addition, organizational, system specific  requirements, or local site policy may require changes as well, or an exception to a  Recommendation or group of Recommendations (e.g. A Benchmark could Recommend  that a Web server not be installed on the system, but if a system's primary purpose is to  function as a Webserver, there should be a documented exception to this  Recommendation for that specific server). 

In the end, exceptions to some Benchmark Recommendations are common and  acceptable, and should be handled as follows: 

• The reasons for the exception should be reviewed cross-functionally and be well  documented for audit purposes. 

• A plan should be developed for mitigating, or eliminating, the exception in the  future, if applicable. 

• If the organization decides to accept the risk of this exception (not work toward  mitigation or elimination), this should be documented for audit purposes. 

It is the responsibility of the organization to determine their overall security policy, and  which settings are applicable to their unique needs based on the overall risk profile for  the organization.

Page 9 

Internal Only \- General   
**Remediation** 

CIS has developed Build Kits for many technologies to assist in the automation of  hardening systems. Build Kits are designed to correspond to Benchmark's  “Remediation” section, which provides the manual remediation steps necessary to make  that Recommendation compliant to the Benchmark. 

| When remediating systems (changing configuration settings on  deployed systems as per the Benchmark's Recommendations),  please approach this with caution and test thoroughly. |
| :---: |

The following is a reasonable remediation approach to follow: 

• CIS Build Kits, or internally developed remediation methods should never be  applied to production systems without proper testing. 

• Proper testing consists of the following: 

o Understand the configuration (including installed applications) of the targeted  systems. Various parts of the organization may need different configurations  (e.g., software developers vs standard office workers). 

o Read the Impact section of the given Recommendation to help determine if  there might be an issue with the targeted systems. 

o Test the configuration changes with representative lab system(s). If issues  arise during testing, they can be resolved prior to deploying to any production  systems. 

o When testing is complete, initially deploy to a small sub-set of production  systems and monitor closely for issues. If there are issues, they can be  resolved prior to deploying more broadly. 

o When the initial deployment above is completes successfully, iteratively  deploy to additional systems and monitor closely for issues. Repeat this  process until the full deployment is complete.  

**Summary** 

Using the Benchmarks Certified tools, working as a team with key stakeholders, being  selective with exceptions, and being careful with remediation deployment, it is possible  to harden large numbers of deployed systems in a cost effective, efficient, and safe  manner. 

**NOTE**: As previously stated, the PDF versions of the CIS Benchmarks™ are  available for free, non-commercial use on the CIS Website. All other formats  of the CIS Benchmarks™ (MS Word, Excel, and Build Kits) are available for  CIS SecureSuite® members. 

CIS-CAT® Pro is also available to CIS SecureSuite® members.

Page 10 

Internal Only \- General   
**Target Technology Details** 

This document provides prescriptive guidance for establishing a secure configuration  posture for Google Chrome browser. This guide was tested against Google Chrome  v138. To obtain the latest version of this guide, please visit  

http://benchmarks.cisecurity.org. If you have questions, comments, or have identified  ways to improve this guide, please write us at feedback@cisecurity.org. 

**Intended Audience** 

The Google Chrome CIS Benchmarks are written for Google Chrome managed using  Google Workspace, not standalone/workgroup systems. Adjustments/tailoring to some  recommendations will be needed to maintain functionality if attempting to implement  CIS hardening on standalone systems.

Page 11 

Internal Only \- General   
**Consensus Guidance** 

This CIS Benchmark™ was created using a consensus review process comprised of a  global community of subject matter experts. The process combines real world  experience with data-based information to create technology specific guidance to assist  users to secure their environments. Consensus participants provide perspective from a  diverse set of backgrounds including consulting, software development, audit and  compliance, security research, operations, government, and legal.  

Each CIS Benchmark undergoes two phases of consensus review. The first phase  occurs during initial Benchmark development. During this phase, subject matter experts  convene to discuss, create, and test working drafts of the Benchmark. This discussion  occurs until consensus has been reached on Benchmark recommendations. The  second phase begins after the Benchmark has been published. During this phase, all  feedback provided by the Internet community is reviewed by the consensus team for  incorporation in the Benchmark. If you are interested in participating in the consensus  process, please visit https://workbench.cisecurity.org/.

Page 12 

Internal Only \- General   
**Typographical Conventions** 

The following typographical conventions are used throughout this guide:

| Convention  | Meaning |
| :---- | :---- |
| Stylized Monospace font | Used for blocks of code, command, and  script examples. Text should be interpreted  exactly as presented. |
| Monospace font | Used for inline code, commands, UI/Menu  selections or examples. Text should be  interpreted exactly as presented. |
| \<Monospace font in brackets\>  | Text set in angle brackets denote a variable  requiring substitution for a real value. |
| *Italic font* | Used to reference other relevant settings,  CIS Benchmarks and/or Benchmark  Communities. Also, used to denote the title  of a book, article, or other publication. |
| **Bold font** | Additional information or caveats things like  **Notes**, **Warnings**, or **Cautions** (usually just  the word itself and the rest of the text  normal). |

Page 13 

Internal Only \- General   
**Recommendation Definitions** 

The following defines the various components included in a CIS recommendation as  applicable. If any of the components are not applicable it will be noted, or the  component will not be included in the recommendation.  

**Title** 

Concise description for the recommendation's intended configuration.  **Assessment Status**   
An assessment status is included for every recommendation. The assessment status  indicates whether the given recommendation can be automated or requires manual  steps to implement. Both statuses are equally important and are determined and  supported as defined below:  

**Automated** 

Represents recommendations for which assessment of a technical control can be fully  automated and validated to a pass/fail state. Recommendations will include the  necessary information to implement automation. 

**Manual** 

Represents recommendations for which assessment of a technical control cannot be  fully automated and requires all or some manual steps to validate that the configured  state is set as expected. The expected state can vary depending on the environment. 

**Profile** 

A collection of recommendations for securing a technology or a supporting platform.  Most benchmarks include at least a Level 1 and Level 2 Profile. Level 2 extends Level 1  recommendations and is not a standalone profile. The Profile Definitions section in the  benchmark provides the definitions as they pertain to the recommendations included for  the technology.  

**Description** 

Detailed information pertaining to the setting with which the recommendation is  concerned. In some cases, the description will include the recommended value. 

**Rationale Statement** 

Detailed reasoning for the recommendation to provide the user a clear and concise  understanding on the importance of the recommendation.

Page 14 

Internal Only \- General   
**Impact Statement**  

Any security, functionality, or operational consequences that can result from following  the recommendation. 

**Audit Procedure**  

Systematic instructions for determining if the target system complies with the  recommendation. 

**Remediation Procedure** 

Systematic instructions for applying recommendations to the target system to bring it  into compliance according to the recommendation. 

**Default Value** 

Default value for the given setting in this recommendation, if known. If not known, either  not configured or not defined will be applied.  

**References** 

Additional documentation relative to the recommendation.  

**CIS Critical Security Controls® (CIS Controls®)** 

The mapping between a recommendation and the CIS Controls is organized by CIS  Controls version, Safeguard, and Implementation Group (IG). The Benchmark in its  entirety addresses the CIS Controls safeguards of (v7) “5.1 \- Establish Secure  Configurations” and (v8) '4.1 \- Establish and Maintain a Secure Configuration Process”  so individual recommendations will not be mapped to these safeguards. 

**Additional Information**  

Supplementary information that does not correspond to any other field but may be  useful to the user. 

Page 15 

Internal Only \- General   
**Profile Definitions**  

The following configuration profiles are defined by this Benchmark: • **Level 1 (L1) \- Corporate/Enterprise Environment (general use)** Items in this profile intend to: 

o be the starting baseline for most organizations; 

o be practical and prudent; 

o provide a clear security benefit; and 

o not inhibit the utility of the technology beyond acceptable means. 

• **Level 2 (L2) \- High Security/Sensitive Data Environment (limited  functionality)** 

This profile extends the "Level 1 (L1)" profile. Items in this profile exhibit one or  more of the following characteristics: 

o are intended for environments or use cases where security is more critical  than manageability and usability; 

o may negatively inhibit the utility or performance of the technology; and o limit the ability of remote management/access. 

Note: Implementation of Level 2 requires that both Level 1 and Level 2 settings  are applied.

Page 16 

Internal Only \- General   
**Acknowledgements** 

This Benchmark exemplifies the great things a community of users, vendors, and  subject matter experts can accomplish through consensus collaboration. The CIS  community thanks the entire consensus team with special recognition to the following  individuals who contributed greatly to the creation of this guide: 

**Contributor**   
Edward Byrd , Center for Internet Security, New York   
Jordan Rakoske 

Brian Howson    
Johannes Goerlich , Siemens AG   
Fletcher Oliver   
Adrian Clark    
Joe Goerlich , Siemens AG   
Patrick Stoeckle , Siemens AG   
John Mahlman    
Joseph Musso   
Loren Hudziak   
Daniel Christopher    
Kari Byrd  

**Editor**   
Phil White , Center for Internet Security, New York   
Edward Byrd , Center for Internet Security, New York   
Josh Franklin 

Page 17 

Internal Only \- General   
**Recommendations** 

**1 Introduction** 

This Benchmark assumes that Google Chrome is managed via Google Workspace. *Recommendation Order* 

This Benchmark has high-level sections based on various security related concerns  (Enforced Defaults, Privacy, etc.). The recommendations are in order of the order in  Google Workspace. 

*Enforced Defaults* 

Many of the settings specified in this Benchmark are also the default settings for the  browser. These are specified for the following reasons: 

1\. The default (Unset) setting may have the same effect as what is prescribed, but  they allow the user to change these settings at any time. Actually configuring the  browser setting to the prescribed value will prevent the user from changing it. 

2\. Many organizations want the ability to scan systems for Benchmark compliance  and configuration drift using CIS (CIS-CAT) or CIS certified third party tools (CIS  Vendor Partners). Having these settings specified in the Benchmark allows for  this. 

*Viewing the Resulting "Policies" in Chrome* 

These "Policy" settings can be viewed in Google Chrome directly by typing  chrome://policy/ directly into the Google Chrome address box, or through Google  Workspace, https://admin.google.com. 

For more information on Google Chrome Enterprise Core Browser management, visit  https://chromeenterprise.google/products/cloud-management/

Page 18 

Internal Only \- General   
**2 Settings** 

Settings is a high level configuration option in the Google admin console for managing  user and organization settings for the Google Chrome Browser.

Page 19 

Internal Only \- General   
**2.1 Sign-in Settings** 

The Google Chrome Admin Sign-in settings are the configuration options for managing  user access and data synchronization on Chrome browsers within an organization  within the Google Admin console. Administrators can control how users sign in to the  Chrome browser on managed devices, including whether they can sign in at all, which  accounts they can use, and whether they can sync their browser data to their Google  account.

Page 20 

Internal Only \- General   
*2.1.1 (L2) Ensure 'Browser sign in settings' is set to 'Disabled  browser sign-in' (Automated)* 

**Profile Applicability:** 

• Level 2 (L2) \- High Security/Sensitive Data Environment (limited functionality) **Description:** 

Google Chrome offers to sign in with your Google account and use account-related  services like Chrome sync. It is possible to sign in to Google Chrome with a Google  account to use services like synchronization, and can also be used for configuration and  management of the browser. 

• Disable browser sign-in (0) 

• Enable browser sign-in (1) 

• Force users to sign-in to use the browser (2) 

The recommended state for this setting is: Enabled with a value of Disable browser  sign-in (0) 

**NOTE:** If an organization is a Google Workspace Enterprise customer, they will want to  leave this setting enabled so that users can sign in with Google accounts. 

**Rationale:** 

Since external accounts are unmanaged and potentially used to access several private  computer systems and many different websites, connecting accounts via sign-in poses  a security risk for the company. It interferes with the corporate management  mechanisms, as well as permits an unwanted leak of corporate information and possible  mixture with private, non-company data. 

**Impact:** 

If this setting is configured, the user cannot sign in to the browser and use Google  account-based services like Chrome sync. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Browser sign in settings 6\. Ensure Configuration is set to Disabled browser sign-in

Page 21 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Browser sign in settings 6\. Set Configuration to Disabled browser sign-in 

7\. Select Save 

**Default Value:** 

Unset (Same as Enabled: Enable browser sign-in, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#BrowserSignin 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 9.2 Use DNS Filtering Services  Use DNS filtering services on all enterprise assets to block access to known  malicious domains. | ●  | ●  | ● |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 22 

Internal Only \- General   
*2.1.2 (L1) Ensure 'Azure Cloud Authentication' Is Set to 'Enable  Azure cloud authentication' (Manual)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This policy setting allows accounts backed by a Microsoft® cloud identity provider (i.e.,  Microsoft Azure Active Directory or the consumer Microsoft account identity provider) to  be signed into web properties using that identity automatically. It can be configured to  either: 

• Disabled (0): Disable Microsoft® cloud authentication 

• Enabled (1): Enable Microsoft® cloud authentication 

If the value for CloudAPAuthEnabled is not changed from the default, it will behave as if  it is disabled. 

**Rationale:** 

Enabling this policy setting allows users to use Microsoft Cloud Authentication for any  site that requires CA (Cloud Authentication) and does not require an extension. 

**Impact:** 

There should be no impact to the user. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Azure Cloud Authentication 6\. Ensure Configuration is set to Enable Azure cloud authentication

Page 23 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Azure Cloud Authentication 6\. Set Configuration to Enable Azure cloud authentication 

7\. Select Save 

**Default Value:** 

Unset (Disabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#CloudAPAuthEnabled 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 9.2 Use DNS Filtering Services  Use DNS filtering services on all enterprise assets to block access to known  malicious domains. | ●  | ●  | ● |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 24 

Internal Only \- General   
**2.2 Apps and Extensions** 

Apps and extensions settings are configuration options in the Google admin console for  control which applications and browser extensions users can install and use on their  Chrome browsers within an organization. 

Administrators can block unwanted apps, force-install necessary ones, and manage  access to specific features by setting policies for each app or extension within the  organization.

Page 25 

Internal Only \- General   
*2.2.1 (L2) Ensure 'Manifest v2 extension availability' Is Set to  'Enable force-installed manifest v2 extensions on the sign-in  screen' (Automated)* 

**Profile Applicability:** 

• Level 2 (L2) \- High Security/Sensitive Data Environment (limited functionality) **Description:** 

This policy setting controls extension management settings for Google Chrome,  specifically v2 extensions. This policy setting is being sunsetted as Google develops the  Manifest v3, but that rollout is currently postponed. 

The policy can be configured to: 

• Default (0): Default browser behavior 

• Disabled (1): Manifest v2 is disabled 

• Enabled (2): Manifest v2 is enabled 

• Forced Only (3): Manifest v2 is enabled for forced extensions only 

**Rationale:** 

Setting this to Forced Only will not allow users to install any additional v2 extensions,  and all existing, non-forced, v2 extensions will be disabled. 

**Impact:** 

Users that use extensions regularly will have a set of them blocked, which will change  their user experience. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Manifest v2 extension  availability 

6\. Ensure Configuration is set to Enable force-installed manifest v2  extensions on the sign-in screen

Page 26 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Manifest v2 extension  availability 

6\. Set Configuration to Enable force-installed manifest v2 extensions  on the sign-in screen 

7\. Select Save 

**References:** 

1\. https://chromeenterprise.google/policies/\#ExtensionManifestV2Availability **CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 7.2 Establish and Maintain a Remediation Process Establish and maintain a risk-based remediation strategy documented in a  remediation process, with monthly, or more frequent, reviews. | ●  | ●  | ● |
| v7 | 9.4 Apply Host-based Firewalls or Port Filtering Apply host-based firewalls or port filtering tools on end systems, with a  default-deny rule that drops all traffic except those services and ports that are  explicitly allowed. | ●  | ●  | ● |

Page 27 

Internal Only \- General   
**2.3 Site Isolation** 

Site isolation settings are configuration options in the Google admin console for isolating  all sites, or only specific origins, on Chrome browsers within an organization. 

Administrators can control whether different websites load in separate processes within  the browser, effectively isolating them from each other to enhance security by  preventing malicious sites from accessing sensitive data from other websites,  essentially acting as a critical security feature to protect against cross-site attacks like  Spectre and Meltdown.

Page 28 

Internal Only \- General   
*2.3.1 (L1) Ensure 'Site isolation' is set to 'Require Site Isolation for  all websites, as well as any origins below' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls if every website will load into its own process. 

Disabled (0): Doesn't turn off site isolation, but it lets users opt out. The recommended state for this setting is: Enabled (1) 

**Rationale:** 

Chrome will load each website in its own process. Even if a site bypasses the same origin policy, the extra security will help stop the site from stealing your data from  another website. 

**Impact:** 

If the policy is enabled, each site will run in its own process which will cause the system  to use more memory. You might want to look at the Enable Site Isolation for  specified origins policy setting to get the best of both worlds – isolation and limited  impact for users – by using Enable Site Isolation for specified origins with a  list of the sites you want to isolate. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Site isolation 

6\. Ensure Configuration is set to Require Site Isolation for all  websites, as well as any origins below

Page 29 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Site isolation 

6\. Set Configuration to Require Site Isolation for all websites, as  well as any origins below 

7\. Select Save 

**Default Value:** 

Unset (Same as Disabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#SitePerProcess   
2\. https://www.chromium.org/Home/chromium-security/site-isolation 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 8.3 Ensure Adequate Audit Log Storage  Ensure that logging destinations maintain adequate storage to comply with  the enterprise’s audit log management process. | ●  | ●  | ● |
| v7 | 10.5 Ensure Backups Have At least One Non Continuously Addressable Destination  Ensure that all backups have at least one backup destination that is not  continuously addressable through operating system calls. | ●  | ●  | ● |

Page 30 

Internal Only \- General   
**2.4 Security** 

Security settings are configuration options in the Google admin console for managing  various security aspects of Chrome browsers within an organization. 

Administrators can control features like blocking specific websites, managing  extensions, enforcing password policies, controlling site permissions, and setting Safe  Browsing protection levels, all aimed at enhancing user security and preventing  potential threats.

Page 31 

Internal Only \- General   
*2.4.1 (L1) Ensure 'Password manager' is Explicitly Configured  (Manual)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

Google Chrome has a built-in password manager to store passwords for users. Chrome  will use local authentication to allow users to gain access to these passwords. 

The recommended state for this setting is: Explicitly set to Enabled (1) or Disabled (0)  based on the organization's needs. 

**NOTE:** If you choose to Enable this setting, please review Disable synchronization  of data with Google and ensure this setting is configured to meet organizational  requirements. 

**Rationale:** 

The Google Chrome password manager is Enabled by default and each organization  should review and determine if they want to allow users to store passwords in the  Browser. If another solution is used instead of the built-in Chrome option then an  organization should configure the setting to Disabled. 

**Impact:** 

Organizationally dependent. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Password manager 6\. Ensure Configuration is set to Always allow use of password manager or  Never allow use of password manager

Page 32 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Password manager 

6\. Set Configuration to Always allow use of password manager or Never  allow use of password manager 

7\. Select Save 

**Default Value:** 

Unset (Same as Enabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#PasswordManagerEnabled   
2\. https://www.ncsc.gov.uk/blog-post/what-does-ncsc-think-password-managers 3\. https://pages.nist.gov/800-63-3/sp800-63b.html 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 9.2 Use DNS Filtering Services  Use DNS filtering services on all enterprise assets to block access to known  malicious domains. | ●  | ●  | ● |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 33 

Internal Only \- General   
*2.4.2 (L1) Ensure 'Web Authentication requests on sites with  broken TLS certificates' Is Set to 'Do not allow WebAuthn API  requests on sites with broken TLS certificates' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This policy setting controls the WebAuthn API and its interaction with sites that have a  broken TLS certificate. It can be configured to either: 

• Disabled (0): Do not allow WebAuthn API requests on sites with  broken TLS certificates. 

• Enabled (1): Allow WebAuthn API requests on sites with broken TLS  certificates. 

If the value for AllowWebAuthnWithBrokenTlsCerts is not changed from the default, it  will behave as it is disabled.xempt. 

**Rationale:** 

Setting this policy will block the ability to authenticate to any website that does not have  a valid TLS certificate since the identity of the site cannot be verified. 

**Impact:** 

There should be no user impact. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Web Authentication requests on  sites with broken TLS certificates 

6\. Ensure Configuration is set to Do not allow WebAuthn API requests on  sites with broken TLS certificates

Page 34 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Web Authentication requests on  sites with broken TLS certificates 

6\. Set Configuration to Do not allow WebAuthn API requests on sites  with broken TLS certificates 

7\. Select Save 

**Default Value:** 

Unset (Disabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#AllowWebAuthnWithBrokenTlsCerts **CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 3.10 Encrypt Sensitive Data in Transit  Encrypt sensitive data in transit. Example implementations can include:  Transport Layer Security (TLS) and Open Secure Shell (OpenSSH). |  | ●  | ● |
| v8 | 14.4 Train Workforce on Data Handling Best Practices Train workforce members on how to identify and properly store, transfer, archive,  and destroy sensitive data. This also includes training workforce members on clear  screen and desk best practices, such as locking their screen when they step away  from their enterprise asset, erasing physical and virtual whiteboards at the end of  meetings, and storing data and assets securely. | ●  | ●  | ● |

Page 35 

Internal Only \- General   
*2.4.3 (L1) Ensure 'Post-quantum TLS' Is Set to 'Allow post quantum key agreement in TLS connections' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This configures whether Google Chrome will offer a post-quantum key agreement  algorithm in TLS, using the ML-KEM NIST standard, and will protect user traffic from  quantum computers when communicating with compatible servers. Enabling a post quantum key agreement is backwards compatible, so there will be no issue with existing  TLS servers. 

**Rationale:** 

This will protect user traffic from quantum computer decrypting. 

**Impact:** 

There should be no impact on the user 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Post-quantum TLS 

6\. Ensure Configuration is set to Allow post-quantum key agreement in  TLS connections 

**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Post-quantum TLS 

6\. Set Configuration to Allow post-quantum key agreement in TLS  connections 

7\. Select Save

Page 36 

Internal Only \- General   
**References:** 

1\. https://chromeenterprise.google/policies/\#PostQuantumKeyAgreementEnabled **CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | :---- | :---: | ----- |
| v8 | 3.10 Encrypt Sensitive Data in Transit  Encrypt sensitive data in transit. Example implementations can include:  Transport Layer Security (TLS) and Open Secure Shell (OpenSSH). |  | ●  | ● |
| v7  | 14.4 Encrypt All Sensitive Information in Transit Encrypt all sensitive information in transit.  |  | ●  | ● |

Page 37 

Internal Only \- General   
*2.4.4 (L1) Ensure 'Incognito mode' is set to 'Disallow incognito  mode' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

Specifies whether the user may open pages in Incognito mode in Google Chrome. The  possible values are: 

• Incognito mode available (0 \- Same as Disabled)) 

• Incognito mode disabled (1) 

• Incognito mode forced (2) 

The recommended state for this setting is: Enabled: Incognito mode disabled (1) **Rationale:** 

Incognito mode in Chrome gives you the choice to browse the internet without your  activity being saved to your browser or device. 

Allowing users to use the browser without any information being saved can hide  evidence of malicious behaviors. This information may be important for a computer  investigation, and investigators such as Computer Forensics Analysts may not be able  to retrieve pertinent information to the investigation. 

**Impact:** 

Users will not be able to initiate Incognito mode for Google Chrome. **Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Incognito mode 

6\. Ensure Configuration is set to Disallow incognito mode

Page 38 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Incognito mode 

6\. Set Configuration to Disallow incognito mode 

7\. Select Save 

**Default Value:** 

Unset (Same as Enabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#IncognitoModeAvailability **CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Internal Only \- General 

Page 39   
*2.4.5 (L1) Ensure 'Browser history' is set to 'Always save browser  history' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

Google Chrome is configured to save the browser history. 

The recommended state for this setting is: Always save browser history 

**NOTE:** This setting will preserve browsing history that could contain a user's personal  browsing history. Please make sure that this setting is in compliance with organizational  policies. 

**Rationale:** 

Browser history shall be saved as it may contain indicators of compromise. **Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Browser history 

6\. Ensure Configuration is set to Always save browser history 

**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Browser history 

6\. Set Configuration to Always save browser history 

7\. Select Save

Page 40 

Internal Only \- General   
**Default Value:** 

Unset (Same as Disabled, but user can change). 

**References:** 

1\. https://chromeenterprise.google/policies/\#SavingBrowserHistoryDisabled **CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | ----- | ----- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7 | 3.5 Deploy Automated Software Patch Management  Tools  Deploy automated software update tools in order to ensure that third-party  software on all systems is running the most recent security updates provided by  the software vendor. | ●  | ●  | ● |

Page 41 

Internal Only \- General   
*2.4.6 (L1) Ensure 'Clear browser history' Is Set to 'Do not allow  clearing history in settings menu' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

Google Chrome can delete the browser and download history using the clear browsing  data menu. 

The recommended state for this setting is: Disabled (0) 

**NOTE:** Even when this setting is disabled, the browsing and download history aren't  guaranteed to be retained. Users can edit or delete the history database files directly,  and the browser itself may remove (based on expiration period) or archive any or all  history items at any time 

**Rationale:** 

If users can delete websites they have visited or files they have downloaded it will be  easier for them to hide evidence that they have visited unauthorized or malicious sites. 

**Impact:** 

If this setting is disabled, browsing and download history cannot be deleted by using the  clear browsing data menu. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Clear browser history 6\. Ensure Configuration is set to Do not allow clearing history in  settings menu

Page 42 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Clear browser history 

6\. Set Configuration to Do not allow clearing history in settings menu 7\. Select Save 

**Default Value:** 

Unset (Same as Enabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#AllowDeletingBrowserHistory **CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 9.2 Use DNS Filtering Services  Use DNS filtering services on all enterprise assets to block access to known  malicious domains. | ●  | ●  | ● |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 43 

Internal Only \- General   
*2.4.7 (L1) Ensure 'Force ephemeral mode' is set to 'Do not erase  local user data' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls whether user profiles are switched to ephemeral mode. In  ephemeral mode, profile data is saved on disk for the length of the session and then the  data is deleted after the session is over. Therefore, no data is saved to the device. 

The recommended state for this setting is: Do not erase local user data **Rationale:** 

Allowing use of ephemeral profiles allows a user to use Google Chrome with no data  being logged to the system. Deleting browser data will delete information that may be  important for a computer investigation and investigators such as Computer Forensics  Analysts may not be able to retrieve pertinent information to the investigation. 

**Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Force ephemeral mode 6\. Ensure Erase local data when the browser is closed is set to Do not  erase local user data

Page 44 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Force ephemeral mode 

6\. Set Erase local data when the browser is closed to Do not erase  local user data 

7\. Select Save 

**Default Value:** 

Unset (Same as Disabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#ForceEphemeralProfiles 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 9.2 Use DNS Filtering Services  Use DNS filtering services on all enterprise assets to block access to known  malicious domains. | ●  | ●  | ● |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 45 

Internal Only \- General   
*2.4.8 (L1) Ensure 'Online revocation checks' is set to 'Perform  online OCSP/CRL checks' (Automated)* 

**Profile Applicability:** 

• Level 2 (L2) \- High Security/Sensitive Data Environment (limited functionality) **Description:** 

Google Chrome performs revocation checking for server certificates that successfully  validate and are signed by locally-installed CA certificates. If Google Chrome is unable  to obtain revocation status information, such certificates will be treated as revoked  ('hard-fail'). 

Disabled: Google Chrome uses existing online revocation-checking settings. The recommended state for this setting is: Enabled (1) 

**Rationale:** 

Certificates shall always be validated. 

**Impact:** 

A revocation check will be performed for server certificates that successfully validate  and are signed by locally-installed CA certificates. if the OCSP server goes down, then  this will hard-fail and prevent browsing to those sites. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Online revocation checks 6\. Ensure Configuration is set to Perform online OCSP/CRL checks

Page 46 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Online revocation checks 6\. Set Configuration to Perform online OCSP/CRL checks 

7\. Select Save 

**Default Value:** 

Unset (Same as Disabled, and users can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#RequireOnlineRevocationChecksForLo calAnchors 

**CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Page 47 

Internal Only \- General   
*2.4.9 (L1) Ensure 'Geolocation' is set to 'Do not allow sites to  detect users' geolocation' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) **Description:** 

Google Chrome supports tracking a user's physical location using GPS, data about  nearby Wi-Fi access points or cellular signal sites/towers (even if you’re not using  them), and your computer’s IP. 

• Disabled (0, same as 3\) 

• Allow sites to track the users' physical location (1) • Do not allow any site to track the users' physical location (2) • Ask whenever a site wants to track the users' physical location (3) 

The recommended state for this setting is: Enabled with a value Do not allow any  site to track the users' physical location (2) 

**Rationale:** 

From a privacy point of view it is not desirable to submit indicators regarding the  location of the device, since the processing of this information cannot be determined.  Furthermore, this may leak information about the network infrastructure around the  device. 

**Impact:** 

If this setting is disabled, chrome will no longer send data about nearby Wi-Fi access  points or cellular signal sites/towers (even if you’re not using them), and your  computer’s IP address to Google. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Geolocation 

6\. Ensure Configuration is set to Do not allow sites to detect users'  geolocation

Page 48 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Geolocation 

6\. Set Configuration to Do not allow sites to detect users'  

geolocation 

7\. Select Save 

**Default Value:** 

Unset (Same as Disabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#DefaultGeolocationSetting   
2\. https://www.w3.org/2010/api-privacy-ws/papers/privacy-ws-24.pdf 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | :---- | ----- | ----- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 49 

Internal Only \- General   
*2.4.10 (L1) Ensure 'Allowed certificate transparency URLs' is Not  Set (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

Google Chrome can specify URLs/hostnames for which Certificate Transparency will  not be enforced. If this setting is disabled, no URLs are excluded from Certificate  Transparency requirements. 

The recommended state for this setting is: Disabled (0) 

**Rationale:** 

Certificates that are required to be disclosed via Certificate Transparency shall be  treated for all URLs as untrusted if they are not disclosed according to the Certificate  Transparency policy. 

**Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Allowed certificate  transparency URLs 

6\. Ensure Allowed certificate transparency URLs is empty

Page 50 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Allowed certificate  

transparency URLs 

6\. Remove all URLs from Allowed certificate transparency URLs 

7\. Select Save 

**Default Value:** 

Unset (Same as Disabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#CertificateTransparencyEnforcementDi sabledForUrls 

**CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Page 51 

Internal Only \- General   
*2.4.11 (L1) Ensure 'Certificate transparency CA allowlist' is Not  Set (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) **Description:** 

Google Chrome can exclude certificates by their subjectPublicKeyInfo hashes from  enforcing Certificate Transparency requirements. If this setting is disabled, no  certificates are excluded from Certificate Transparency requirements. 

The recommended state for this setting is: Disabled (0) 

**Rationale:** 

Certificate Transparency requirements shall be enforced for all certificates. **Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Certificate transparency CA  allowlist 

6\. Ensure Certificate transparency CA allowlist is empty 

**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Certificate transparency CA  allowlist 

6\. Remove all CAs from Certificate transparency CA allowlist 7\. Select Save

Page 52 

Internal Only \- General   
**Default Value:** 

Unset (Same as Disabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#CertificateTransparencyEnforcementDi sabledForCas 

**CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Page 53 

Internal Only \- General   
*2.4.12 (L1) Ensure 'Renderer App Container' Is Set to 'Enable the  Renderer App Container sandbox' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls the ability for Google Chrome to allow the Render App Container  sandbox to be used while navigating to certain sites. It can be configured to either: 

• Disabled (0): Disable the Renderer App Container sandbox • Enabled (1): Enable the Renderer App Container sandbox 

If the value for RendererAppContainerEnabled is not changed from the default, it will  behave as if it is enabled. 

**Rationale:** 

Disabling this policy would weaken the sandbox that Google Chrome uses for the  renderer process, and will have a detrimental effect on the security and stability of the  browser. This policy needs to be enabled to maintain security and stability. 

**Impact:** 

This would only impact users if there is third-party software that must run inside  renderer processes. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Renderer App Container 6\. Ensure Configuration is set to Enable the Renderer App Container  sandbox

Page 54 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Renderer App Container 6\. Set Configuration to Enable the Renderer App Container sandbox 7\. Select Save 

**Default Value:** 

Unset (Enabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#RendererAppContainerEnabled **CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 9.2 Use DNS Filtering Services  Use DNS filtering services on all enterprise assets to block access to known  malicious domains. | ●  | ●  | ● |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 55 

Internal Only \- General   
*2.4.13 (L1) Ensure 'Enable leak detection for entered credentials'  Is Set to 'Enable Leak detection for entered credentials' (Manual)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This policy controls the ability for Google Chrome to verify if any entered credentials  were part of a leak. If a user's credentials are compromised, the user will be alerted.  The password is not stored on Google's servers, unless Password Sync is enabled, and  is encrypted with a secret key known only to your device. To find out more on how  Google protects your password, see their support article How Chrome protects your  passwords. 

**Note:** This setting has no effect if Safe Browsing is not enabled. 

**Rationale:** 

Users should be aware if any of their credentials have been compromised or leaked. **Impact:** 

There should be no impact on the user. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Enable leak detection for entered credentials 6\. Ensure Configuration is set to Users enrolled in the Advanced  Protection program will receive extra protections

Page 56 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Enable leak detection for entered credentials 6\. Set Configuration to Users enrolled in the Advanced Protection  program will receive extra protections 

7\. Select Save 

**Default Value:** 

Unset (Allow the user to decide) 

**References:** 

1\. https://chromeenterprise.google/policies/\#PasswordLeakDetectionEnabled 2\. https://support.google.com/chrome/a/answer/13597868?hl=en 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 9.2 Use DNS Filtering Services  Use DNS filtering services on all enterprise assets to block access to known  malicious domains. | ●  | ●  | ● |
| v7 | 4.8 Log and Alert on Changes to Administrative Group  Membership  Configure systems to issue a log entry and alert when an account is added  to or removed from any group assigned administrative privileges. |  | ●  | ● |

Page 57 

Internal Only \- General   
*2.4.14 (L1) Ensure 'Audio sandbox' is set to 'Always sandbox the  audio process' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls whether audio processes in Google Chrome run in a sandbox. 

**NOTE:** Security software setups within your environment might interfere with the  sandbox. 

The recommended state for this setting is: Enabled (1) 

**Rationale:** 

Having audio processes run in a sandbox ensures that if a website misuses audio  processes that data may not be manipulated or exfiltrated from the system. 

**Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Audio sandbox 

6\. Ensure Configuration is set to Always sandbox the audio process 

**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Audio sandbox 

6\. Set Configuration to Always sandbox the audio process 7\. Select Save

Page 58 

Internal Only \- General   
**Default Value:** 

Unset (Same as Enabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#AudioSandboxEnabled 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 8.3 Ensure Adequate Audit Log Storage  Ensure that logging destinations maintain adequate storage to comply with  the enterprise’s audit log management process. | ●  | ●  | ● |
| v7 | 10.5 Ensure Backups Have At least One Non Continuously Addressable Destination  Ensure that all backups have at least one backup destination that is not  continuously addressable through operating system calls. | ●  | ●  | ● |

Page 59 

Internal Only \- General   
*2.4.15 (L1) Ensure 'Unsupported system warning' is set to 'Allow  Chrome to display warnings when running on an unsupported  system' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

Google Chrome will show a warning that appears when Google Chrome is running on a  computer or operating system that is no longer supported. 

The recommended state for this setting is: Disabled (0) 

**Rationale:** 

The user shall be informed if the used software is no longer supported. **Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Unsupported system warning 6\. Ensure Configuration is set to Allow Chrome to display warnings when  running on an unsupported system 

**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Unsupported system warning 6\. Set Configuration to Allow Chrome to display warnings when running  on an unsupported system 

7\. Select Save

Page 60 

Internal Only \- General   
**Default Value:** 

Unset (Same as Disabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#SuppressUnsupportedOSWarning **CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 2.2 Ensure Authorized Software is Currently Supported  Ensure that only currently supported software is designated as authorized in the  software inventory for enterprise assets. If software is unsupported, yet necessary  for the fulfillment of the enterprise’s mission, document an exception detailing  mitigating controls and residual risk acceptance. For any unsupported software  without an exception documentation, designate as unauthorized. Review the  software list to verify software support at least monthly, or more frequently. | ●  | ●  | ● |
| v7 | 2.2 Ensure Software is Supported by Vendor  Ensure that only software applications or operating systems currently supported  by the software's vendor are added to the organization's authorized software  inventory. Unsupported software should be tagged as unsupported in the inventory  system. | ●  | ●  | ● |

Page 61 

Internal Only \- General   
*2.4.16 (L2) Ensure 'Advanced Protection program' Is Set to 'Users  enrolled in the Advanced Protection program will receive extra  protections' (Manual)* 

**Profile Applicability:** 

• Level 2 (L2) \- High Security/Sensitive Data Environment (limited functionality) **Description:** 

The Advanced Protection Program is a service offered by Google for users whose  accounts contain particularly valuable files or sensitive information. This service  requires at least one passkey or FIDO compliant security key. Since this is an additional  service, and requires the purchase of additional hardware, this is not a scored  recommendation but is recommended for anyone who is already signed up for the  Advanced Protection Program service. 

**Note:** At the time this benchmark was published the Advanced Protection Program was  available at no charge but to use the program your organization may need to purchase  security keys. 

**Rationale:** 

If a user (or organization) has already enabled the Advanced Protection Program, those  user(s) should use the features offered. 

**Impact:** 

There should be no impact on the user. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Advanced Protection program 

6\. Ensure Configuration is set to Users enrolled in the Advanced  Protection program will receive extra protections

Page 62 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Advanced Protection program 

6\. Set Configuration to Users enrolled in the Advanced Protection  program will receive extra protections 

7\. Select Save 

**Default Value:** 

'Users enrolled in the Advanced Protection program will receive extra protections' **References:** 

1\. https://chromeenterprise.google/policies/\#AdvancedProtectionAllowed   
2\. https://landing.google.com/intl/en\_in/advancedprotection/   
3\. https://support.google.com/accounts/answer/7539956?hl=en\#zippy=%2Chow much-does-advanced-protection-cost 

**CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Page 63 

Internal Only \- General   
*2.4.17 (L1) Ensure 'Override insecure origin restrictions' is Not  Set (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) **Description:** 

Google Chrome can use a list of origins (URLs) or hostname patterns (such as  "\*.example.com") for which security restrictions on insecure origins will not apply and  are prevented from being labeled as "Not Secure" in the omnibox. 

The recommended state for this setting is: Disabled (0) 

**Rationale:** 

Insecure contexts shall always be labeled as insecure. 

**Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Override insecure origin  restrictions 

6\. Ensure Origin or hostname patterns to ignore insecure origins  security restrictions is empty

Page 64 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Override insecure origin  restrictions 

6\. Remove all hostnames from Origin or hostname patterns to ignore  insecure origins security restrictions 

7\. Select Save 

**Default Value:** 

Unset (Same as Disabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#OverrideSecurityRestrictionsOnInsecur eOrigin 

**CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Page 65 

Internal Only \- General   
*2.4.18 (L1) Ensure 'Command-line flags' is set to 'Show security  warnings when potentially dangerous command-line flags are  used' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting prevents Google Chrome from showing security warnings that potentially  dangerous command-line flags are in use at its launch. 

The recommended state of this setting is: Enabled (0) 

**Rationale:** 

If Google Chrome is being launched with potentially dangerous flags, this information  should be exposed to the user as a warning. If not, the user may be unintentionally  using non-secure settings and be exposed to security flaws. 

**Impact:** 

None \- This is the default behavior. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Command-line flags 6\. Ensure Configuration is set to Show security warnings when  potentially dangerous command-line flags are used

Page 66 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Command-line flags 

6\. Set Configuration to Show security warnings when potentially  dangerous command-line flags are used 

7\. Select Save 

**Default Value:** 

Unset (Same as Enabled, but user can change) 

**References:** 

1\. https://chromeenterprise.google/policies/\#CommandLineFlagSecurityWarningsE nabled 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 8.3 Ensure Adequate Audit Log Storage  Ensure that logging destinations maintain adequate storage to comply with  the enterprise’s audit log management process. | ●  | ●  | ● |
| v7 | 7.2 Disable Unnecessary or Unauthorized Browser or  Email Client Plugins  Uninstall or disable any unauthorized browser or email client plugins or add on applications. |  | ●  | ● |

Page 67 

Internal Only \- General   
*2.4.19 (L1) Ensure 'Allow remote debugging' is set to 'Do not  allow use of the remote debugging' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This policy setting controls whether users may use remote debugging. This feature  allows remote debugging of live content on a Windows 10 or later device from a  Windows or macOS computer. 

The recommended state for this setting is: Disabled. 

**Rationale:** 

Disabling remote debugging enhances security and protects applications from  unauthorized access. Some attack tools can exploit this feature to extract information,  or to insert malicious code. 

**Impact:** 

Users will not be able access the remote debugging feature in Google Chrome. **Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Allow remote debugging 6\. Ensure Configuration is set to Do not allow use of the remote  debugging 

**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Allow remote debugging 6\. Set Configuration to Do not allow use of the remote debugging 7\. Select Save

Page 68 

Internal Only \- General   
**Default Value:** 

Enabled. (Users may use remote debugging by specifying \--remote-debug-port and \-- remote-debugging-pipe command line switches.) 

**Additional Information:** 

I copied/adjusted this rule from MS Edge, rule 1.41 

**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 7.2 Establish and Maintain a Remediation Process Establish and maintain a risk-based remediation strategy documented in a  remediation process, with monthly, or more frequent, reviews. | ●  | ●  | ● |
| v8 | 13.5 Manage Access Control for Remote Assets Manage access control for assets remotely connecting to enterprise resources.  Determine amount of access to enterprise resources based on: up-to-date anti malware software installed, configuration compliance with the enterprise’s secure  configuration process, and ensuring the operating system and applications are up to-date.  |  | ●  | ● |

Page 69 

Internal Only \- General   
*2.4.20 (L1) Ensure 'TLS encrypted ClientHello' Is 'Enable the TLS  Encrypted ClientHello experiment' (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls the defaults for using Encrypted ClientHello (ECH). ECH is an  extension to TLS and encrypts the initial handshake with a website that can only be  decrypted by that website. Google Chrome may, or may not, use ECH based on 3  factors: sever support, HTTPS DNS record availability, or rollout status. It can be  configured to either: 

• Disabled (0): Disable the TLS Encrypted ClientHello experiment • Enabled (1): Enable the TLS Encrypted ClientHello experiment 

If the value for EncryptedClientHelloEnabled is not changed from the default, it will  behave as it is enabled. 

**Rationale:** 

Previously all handshakes were in the open and could expose sensitive information like  the name of the website that you are connecting to. Setting this policy will allow Google  Chrome to use an encrypted hello, or handshake, with a website where it is supported,  thus not exposing sensitive information. 

**Impact:** 

There should be no impact on the user. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select TLS encrypted ClientHello 6\. Ensure Configuration is set to Enable the TLS Encrypted ClientHello  experiment

Page 70 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select TLS encrypted ClientHello 6\. Set Configuration to Enable the TLS Encrypted ClientHello  

experiment 

7\. Select Save 

**Default Value:** 

Unset (Enabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#EncryptedClientHelloEnabled **CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | :---- | :---: | ----- |
| v8 | 3.10 Encrypt Sensitive Data in Transit  Encrypt sensitive data in transit. Example implementations can include:  Transport Layer Security (TLS) and Open Secure Shell (OpenSSH). |  | ●  | ● |
| v7  | 14.4 Encrypt All Sensitive Information in Transit Encrypt all sensitive information in transit.  |  | ●  | ● |

Page 71 

Internal Only \- General   
*2.4.21 (L1) Ensure 'Strict MIME type checking for worker scripts'  Is Set to 'Require a JavaScript MIME type for worker scripts'  (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls the ability for Google Chrome to upgrade to HTTPS from HTTP  while navigating to certain sites. It can be configured to either: 

• Disabled (0): Scripts for workers (Web Workers, Service Workers,  etc.) use lax MIME type checking. Worker scripts with legacy MIME  types, like text/ascii, will work. 

• Enabled (1): Scripts for workers (Web Workers, Service Workers,  etc.) require a JavaScript MIME type, like text/javascript.  Worker scripts with legacy MIME types, like text/ascii, will be  rejected. 

If the value for StrictMimetypeCheckForWorkerScriptsEnabled is not changed from  the default, it will behave as if it is enabled. 

**Rationale:** 

Setting this policy will require worker scripts to use more secure and strict JavaScript  MIME types and ones with legacy MIME Types will be rejected. 

**Impact:** 

This should have no impact on users. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Strict MIME type checking for  worker scripts 

6\. Ensure Configuration is set to Require a JavaScript MIME type for  worker scripts

Page 72 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Strict MIME type checking for  worker scripts 

6\. Set Configuration to Require a JavaScript MIME type for worker  scripts 

7\. Select Save 

**Default Value:** 

Unset (Enabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#StrictMimetypeCheckForWorkerScripts Enabled 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | :---- | :---: | ----- |
| v8 | 9.4 Restrict Unnecessary or Unauthorized Browser and  Email Client Extensions  Restrict, either through uninstalling or disabling, any unauthorized or  unnecessary browser or email client plugins, extensions, and add-on  applications. |  | ●  | ● |
| v7 | 7.2 Disable Unnecessary or Unauthorized Browser or  Email Client Plugins  Uninstall or disable any unauthorized browser or email client plugins or add on applications. |  | ●  | ● |

Page 73 

Internal Only \- General   
*2.4.22 (L2) Ensure 'Enforce local anchor constraints' Is 'Enforce  constraints in locally added trust anchors' (Automated)* 

**Profile Applicability:** 

• Level 2 (L2) \- High Security/Sensitive Data Environment (limited functionality) **Description:** 

This setting controls constraints encoded into trust anchors loaded from the platform  trust store. It can be configured to either: 

• Disabled (0): Do not enforce constraints in locally added trust  anchors 

• Enabled (1): Enforce constraints in locally added trust anchors 

If the value for EnforceLocalAnchorConstraintsEnabled is not changed from the  default, it will behave as if it is enabled. 

**Rationale:** 

Setting this policy will not allow access to any sites that do not enforce constraints. **Impact:** 

Enabling this might cause certain internal sites to not properly load until they are  updated. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Enforce local anchor  constraints 

6\. Ensure Configuration is set to Enforce constraints in locally added  trust anchors

Page 74 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select Enforce local anchor  

constraints 

6\. Set Configuration to Enforce constraints in locally added trust  anchors 

7\. Select Save 

**Default Value:** 

Unset (Enabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#EnforceLocalAnchorConstraintsEnable d 

**CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Page 75 

Internal Only \- General   
*2.4.23 (L1) Ensure 'File/directory picker without user gesture' Is  Not Set (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls the ability for showOpenFilePicker(), showSaveFilePicker(),  and showDirectoryPicker() web APIs to be called without user interaction. 

If the value for FileOrDirectoryPickerWithoutGestureAllowedForOrigins is not  changed from the default, it will behave as if it is disabled. 

**Rationale:** 

Setting this policy would allow the URLs selected to call the showOpenFilePicker(),  showSaveFilePicker(), and showDirectoryPicker() web APIs without any user  gesture/interaction. This policy does not need to be set for this reason. 

**Impact:** 

Disabling this policy should have no impact on the user. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select File/directory picker without  user gesture 

6\. Ensure Allow file or directory picker APIs to be called without  prior user gesture is empty

Page 76 

Internal Only \- General   
**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under User & browser settings, select File/directory picker without  user gesture 

6\. Remove all URLs from Allow file or directory picker APIs to be  called without prior user gesture 

7\. Select Save 

**Default Value:** 

Unset (Disabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#FileOrDirectoryPickerWithoutGestureAl lowedForOrigins 

**CIS Controls:**

| Controls   Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 7.2 Establish and Maintain a Remediation Process Establish and maintain a risk-based remediation strategy documented in a  remediation process, with monthly, or more frequent, reviews. | ●  | ●  | ● |
| v7 | 9.4 Apply Host-based Firewalls or Port Filtering Apply host-based firewalls or port filtering tools on end systems, with a  default-deny rule that drops all traffic except those services and ports that are  explicitly allowed. | ●  | ●  | ● |

Page 77 

Internal Only \- General   
*2.4.24 (L1) Ensure 'Media picker without user gesture' Is Not  Configured (Automated)* 

**Profile Applicability:** 

• Level 1 (L1) \- Corporate/Enterprise Environment (general use) 

**Description:** 

This setting controls the ability for getDisplayMedia() web API to be called without  user interaction based on sites that are configured in this policy. By default, no site can  call the getDisplayMedia() API for screen capture without a prior user gesture. 

**Rationale:** 

Setting this policy would allow the URLs selected to call the getDisplayMedia() web  APIs without any user gesture/interaction. This policy does not need to be set for this  reason. 

**Impact:** 

Disabling this policy should have no impact on the user. 

**Audit:** 

To verify this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Media picker without user gesture 6\. Ensure Allow screen capture without prior user gesture is empty 

**Remediation:** 

To configure this setting via the Google Workspace Admin Console: 

1\. Log in to https://admin.google.com as an administrator 

2\. Select Devices 

3\. Select Chrome 

4\. Select Settings 

5\. Under Security, select Media picker without user gesture 6\. Remove all URLs from Allow screen capture without prior user  gesture 

7\. Select Save

Page 78 

Internal Only \- General   
**Default Value:** 

Unset (disabled) 

**References:** 

1\. https://chromeenterprise.google/policies/\#ScreenCaptureWithoutGestureAllowed ForOrigins 

**CIS Controls:**

| Controls Version  | Control  |  | IG 1IG 2 IG 3 |  |
| :---: | ----- | :---- | ----- | :---- |
| v8  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |
| v7  | 0.0 Explicitly Not Mapped  Explicitly Not Mapped |  |  |  |

Page 79 

Internal Only \- General 