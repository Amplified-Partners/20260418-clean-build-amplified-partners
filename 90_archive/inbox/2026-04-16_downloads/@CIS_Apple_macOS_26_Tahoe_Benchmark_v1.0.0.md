CIS Apple macOS 26  Tahoe Benchmark 

v1.0.0 \- 10-31-2025

Internal Only \- General   
**Terms of Use** 

Please see the below link for our current terms of use: 

https://www.cisecurity.org/cis-securesuite/cis-securesuite-membership-terms-of-use/ 

For information on referencing and/or citing CIS Benchmarks in 3rd party documentation  (including using portions of Benchmark Recommendations) please contact CIS Legal  (legalnotices@cisecurity.org) and request guidance on copyright usage.  

**NOTE**: It is ***NEVER*** acceptable to host a CIS Benchmark in ***ANY*** format (PDF, etc.)  on a 3rd party (non-CIS owned) site.

Page 1 

Internal Only \- General   
**Table of Contents** 

***Terms of Use..................................................................................................................... 1 Table of Contents ............................................................................................................. 2 Overview............................................................................................................................ 7*** 

**Important Usage Information.................................................................................................... 7 Key Stakeholders....................................................................................................................................7 Apply the Correct Version of a Benchmark.........................................................................................8 Exceptions...............................................................................................................................................8 Remediation ............................................................................................................................................9 Summary..................................................................................................................................................9** 

**Target Technology Details ...................................................................................................... 10 Intended Audience ................................................................................................................... 10 Consensus Guidance............................................................................................................... 11 Typographical Conventions.................................................................................................... 12** 

***Recommendation Definitions ....................................................................................... 13*** **Title............................................................................................................................................. 13** 

**Assessment Status .................................................................................................................. 13 Automated .............................................................................................................................................13 Manual....................................................................................................................................................13** 

**Profile......................................................................................................................................... 13 Description................................................................................................................................ 13 Rationale Statement................................................................................................................. 13 Impact Statement...................................................................................................................... 14 Audit Procedure........................................................................................................................ 14 Remediation Procedure........................................................................................................... 14 Default Value............................................................................................................................. 14 References ................................................................................................................................ 14 CIS Critical Security Controls®(CIS Controls®).................................................................... 14 Additional Information............................................................................................................. 14 Profile Definitions..................................................................................................................... 15 Acknowledgements.................................................................................................................. 16** 

***Recommendations ......................................................................................................... 17*** 

**1 Install Updates, Patches and Additional Security Software ............................................ 17** 1.1 Ensure Apple-provided Software Updates Are Installed (Automated)................................18 1.2 Ensure Download New Updates When Available Is Enabled (Automated)........................23 1.3 Ensure Install of macOS Updates Is Enabled (Automated)................................................26 1.4 Ensure Install Application Updates from the App Store Is Enabled (Automated)...............29

Page 2 

Internal Only \- General   
1.5 Ensure Install Security Responses and System Files Is Enabled (Automated) .................32 1.6 Ensure Software Update Deferment Is Less Than or Equal to 30 Days (Automated)........36 

**2 System Settings..................................................................................................................... 40 2.1 Apple Account ................................................................................................................................41 2.1.1 iCloud .........................................................................................................................................42** 2.1.1.1 Audit iCloud Passwords & Keychain (Manual)..............................................................43 2.1.1.2 Audit iCloud Drive (Manual) ..........................................................................................46 2.1.1.3 Ensure iCloud Drive Document and Desktop Sync Is Disabled (Automated) ..............49 2.1.1.4 Audit Security Keys Used With Apple Accounts (Manual)............................................52 2.1.1.5 Audit Freeform Sync to iCloud (Manual).......................................................................54 2.1.1.6 Audit Find My Mac (Manual) .........................................................................................56 2.1.2 Audit App Store Password Settings (Manual)..................................................................60 **2.2 Network............................................................................................................................................62** 2.2.1 Ensure Firewall Is Enabled (Automated)..........................................................................63 2.2.2 Ensure Firewall Stealth Mode Is Enabled (Automated) ...................................................66 **2.3 General ............................................................................................................................................69 2.3.1 AirDrop & Handoff.....................................................................................................................70** 2.3.1.1 Ensure AirDrop Is Disabled When Not Actively Transferring Files (Automated)..........71 2.3.1.2 Ensure AirPlay Receiver Is Disabled (Automated) .......................................................74 **2.3.2 Date & Time ...............................................................................................................................77** 2.3.2.1 Ensure Set Time and Date Automatically Is Enabled (Automated) ..............................78 2.3.2.2 Ensure the Time Service Is Enabled (Automated)........................................................82 **2.3.3 Sharing.......................................................................................................................................84** 2.3.3.1 Ensure Screen Sharing Is Disabled (Automated) .........................................................85 2.3.3.2 Ensure File Sharing Is Disabled (Automated)...............................................................88 2.3.3.3 Ensure Printer Sharing Is Disabled (Automated) ..........................................................91 2.3.3.4 Ensure Remote Login Is Disabled (Automated)............................................................93 2.3.3.5 Ensure Remote Management Is Disabled (Automated) ...............................................97 2.3.3.6 Ensure Remote Apple Events Is Disabled (Automated) .............................................100 2.3.3.7 Ensure Internet Sharing Is Disabled (Automated) ......................................................102 2.3.3.8 Ensure Content Caching Is Disabled (Automated) .....................................................105 2.3.3.9 Ensure Media Sharing Is Disabled (Automated).........................................................108 2.3.3.10 Ensure Bluetooth Sharing Is Disabled (Automated) .................................................111 

2.3.3.11 Ensure Computer Name Does Not Contain PII or Protected Organizational  Information (Manual) ...............................................................................................................114 **2.3.4 Time Machine ..........................................................................................................................117** 2.3.4.1 Ensure Backup Automatically is Enabled If Time Machine Is Enabled (Automated) .118 2.3.4.2 Ensure Time Machine Volumes Are Encrypted If Time Machine Is Enabled  (Automated).............................................................................................................................122 **2.3.5 Language & Region ................................................................................................................125 2.4 Menu Bar .......................................................................................................................................125** 2.4.1 Audit Menu Bar and Control Center Icons (Manual)......................................................126 **2.5 Apple Intelligence & Siri ..............................................................................................................128 2.5.1 Apple Intelligence ...................................................................................................................129** 2.5.1.1 Ensure External Intelligence Extensions Is Disabled (Automated).............................130 2.5.1.2 Ensure Writing Tools Is Disabled (Automated) ...........................................................133 2.5.1.3 Ensure Mail Summarization Is Disabled (Automated) ................................................136 2.5.1.4 Ensure Notes Summarization Is Disabled (Automated)..............................................139 **2.5.2 Siri.............................................................................................................................................142** 2.5.2.1 Ensure Siri Is Disabled (Automated) ...........................................................................143 2.5.2.2 Ensure Listen for (Siri) Is Disabled (Manual) ..............................................................146 **2.6 Privacy & Security........................................................................................................................149 2.6.1 Location Services ...................................................................................................................150** 2.6.1.1 Ensure Location Services Is Enabled (Automated) ....................................................151

Page 3 

Internal Only \- General   
2.6.1.2 Ensure 'Show Location Icon in Control Center when System Services Request Your  Location' Is Enabled (Automated) ...........................................................................................155 2.6.1.3 Audit Location Services Access (Manual)...................................................................158 

**2.6.2 Full Disk Access......................................................................................................................161** 2.6.2.1 Audit Full Disk Access for Applications (Manual)........................................................162 **2.6.3 Analytics & Improvements.....................................................................................................164** 2.6.3.1 Ensure Share Mac Analytics Is Disabled (Automated) ...............................................165 2.6.3.2 Ensure Improve Siri & Dictation Is Disabled (Automated) ..........................................167 2.6.3.3 Ensure Improve Assistive Voice Features Is Disabled (Automated) ..........................169 2.6.3.4 Ensure 'Share with app developers' Is Disabled (Automated)....................................171 2.6.3.5 Ensure Share iCloud Analytics Is Disabled (Manual) .................................................173 2.6.4 Ensure Limit Ad Tracking Is Enabled (Automated) ........................................................175 2.6.5 Ensure Gatekeeper Is Enabled (Automated) .................................................................177 2.6.6 Ensure FileVault Is Enabled (Automated)......................................................................180 2.6.7 Audit Lockdown Mode (Manual).....................................................................................183 

2.6.8 Ensure an Administrator Password Is Required to Access System-Wide Preferences  (Automated).............................................................................................................................185 **2.7 Desktop & Dock............................................................................................................................189** 2.7.1 Ensure Screen Saver Corners Are Secure (Automated) ...............................................190 2.7.2 Audit iPhone Mirroring (Manual).....................................................................................192 **2.8 Displays.........................................................................................................................................194** 2.8.1 Audit Universal Control Settings (Manual) .....................................................................195 **2.9 Spotlight ........................................................................................................................................198** 2.9.1 Ensure Help Apple Improve Search Is Disabled (Automated).......................................199 **2.10 Battery (Energy Saver)...............................................................................................................201 2.10.1 OS Resuming From Sleep....................................................................................................202** 2.10.1.1 Ensure the OS Is Not Active When Resuming from Standby (Intel) (Manual) .........203 2.10.1.2 Ensure Sleep and Display Sleep Is Enabled on Apple Silicon Devices (Automated) .................................................................................................................................................207 2.10.2 Ensure Power Nap Is Disabled for Intel Macs (Automated) ........................................211 2.10.3 Ensure Wake for Network Access Is Disabled (Automated)........................................215 **2.11 Lock Screen ................................................................................................................................220** 2.11.1 Ensure an Inactivity Interval of 15 Minutes Or Less for the Screen Saver Is Enabled  (Automated).............................................................................................................................221 2.11.2 Ensure Require Password After Screen Saver Begins or Display Is Turned Off Is  Enabled for 5 Seconds or Immediately (Automated) ..............................................................223 2.11.3 Ensure a Custom Message for the Login Screen Is Enabled (Automated) .................227 2.11.4 Ensure Login Window Displays as Name and Password Is Enabled (Automated).....230 2.11.5 Ensure Show Password Hints Is Disabled (Automated) ..............................................232 **2.12 Touch ID & Password (Login Password) .................................................................................235** 2.12.1 Ensure Users' Accounts Do Not Have a Password Hint (Automated).........................236 2.12.2 Audit Touch ID (Manual) ..............................................................................................238 **2.13 Users & Groups ..........................................................................................................................242** 2.13.1 Ensure Guest Account Is Disabled (Automated) .........................................................243 2.13.2 Ensure Guest Access to Shared Folders Is Disabled (Automated) .............................246 2.13.3 Ensure Automatic Login Is Disabled (Automated) .......................................................248 **2.14 Game Center ...............................................................................................................................251** 2.14.1 Audit Game Center Settings (Manual) .........................................................................252 **2.15 Notifications................................................................................................................................255** 2.15.1 Audit Notification Settings (Manual) .............................................................................256 **2.16 Wallet & Apple Pay.....................................................................................................................258** 2.16.1 Audit Wallet & Apple Pay Settings (Manual)................................................................259 **2.17 Internet Accounts.......................................................................................................................261** 2.17.1 Audit Internet Accounts for Authorized Use (Manual)..................................................262 **2.18 Keyboard .....................................................................................................................................265** 2.18.1 Ensure On-Device Dictation Is Enabled (Automated)..................................................266

Page 4 

Internal Only \- General   
**3 Logging and Auditing ......................................................................................................... 268** 3.1 Ensure Security Auditing Is Enabled (Automated)............................................................269 3.2 Ensure Security Auditing Flags For User-Attributable Events Are Configured Per Local  Organizational Requirements (Automated).............................................................................271 3.3 Ensure install.log Is Retained for 365 or More Days and No Maximum Size (Automated) .................................................................................................................................................274 3.4 Ensure Security Auditing Retention Is Enabled (Automated) ...........................................276 3.5 Ensure Access to Audit Records Is Controlled (Automated) ............................................278 3.6 Audit Software Inventory (Manual)....................................................................................282 

**4 Network Configurations...................................................................................................... 284** 4.1 Ensure Bonjour Advertising Services Is Disabled (Automated)........................................285 4.2 Ensure HTTP Server Is Disabled (Automated) .................................................................288 4.3 Ensure NFS Server Is Disabled (Automated) ...................................................................290 

**5 System Access, Authentication and Authorization ........................................................ 292 5.1 File System Permissions and Access Controls........................................................................293** 5.1.1 Ensure Home Folders Are Secure (Automated) ............................................................294 5.1.2 Ensure System Integrity Protection Status (SIP) Is Enabled (Automated) ....................297 5.1.3 Ensure Apple Mobile File Integrity (AMFI) Is Enabled (Automated) ..............................300 5.1.4 Ensure Signed System Volume (SSV) Is Enabled (Automated)....................................302 5.1.5 Ensure Appropriate Permissions Are Enabled for System Wide Applications (Automated) .................................................................................................................................................304 5.1.6 Ensure No World Writable Folders Exist in the System Folder (Automated) ................306 5.1.7 Ensure No World Writable Folders Exist in the Library Folder (Automated) .................308 **5.2 Account and Password Policy Management.............................................................................310** 5.2.1 Ensure Password Account Lockout Threshold Is Configured (Automated)...................312 5.2.2 Ensure Password Minimum Length Is Configured (Automated)....................................314 

5.2.3 Ensure Complex Password Must Contain Alphabetic Characters Is Configured (Manual) .................................................................................................................................................316 5.2.4 Ensure Complex Password Must Contain Numeric Character Is Configured (Manual) 318 5.2.5 Ensure Complex Password Must Contain Special Character Is Configured (Manual)..320 5.2.6 Ensure Complex Password Must Contain Uppercase and Lowercase Characters Is  Configured (Manual)................................................................................................................322 5.2.7 Ensure Password Age Is Configured (Automated) ........................................................324 5.2.8 Ensure Password History Is Set to at least 24 (Automated)..........................................326 

**5.3 Encryption.....................................................................................................................................328** 5.3.1 Ensure all user storage APFS volumes are encrypted (Manual)...................................329 5.3.2 Ensure all user storage CoreStorage volumes are encrypted (Manual)........................333 5.4 Ensure the Sudo Timeout Period Is Set to Zero (Automated) ..........................................337 5.5 Ensure a Separate Timestamp Is Enabled for Each User/tty Combo (Automated)..........339 5.6 Ensure the "root" Account Is Disabled (Automated) .........................................................342 5.7 Ensure an Administrator Account Cannot Login to Another User's Active and Locked  

Session (Automated)...............................................................................................................345 5.8 Ensure a Login Window Banner Exists (Automated) ........................................................348 5.9 Ensure the Guest Home Folder Does Not Exist (Automated)...........................................351 5.10 Ensure XProtect Is Running and Updated (Automated) .................................................353 5.11 Ensure Logging Is Enabled for Sudo (Automated) .........................................................356 

**6 Applications......................................................................................................................... 358 6.1 Finder.............................................................................................................................................359** 6.1.1 Audit Show All Filename Extensions (Manual) ..............................................................360 **6.2 Mail.................................................................................................................................................363** 6.2.1 Ensure Protect Mail Activity in Mail Is Enabled (Manual)...............................................364 **6.3 Safari..............................................................................................................................................366** 6.3.1 Ensure Automatic Opening of Safe Files in Safari Is Disabled (Automated).................367 6.3.2 Audit History and Remove History Items (Manual) ........................................................369

Page 5 

Internal Only \- General   
6.3.3 Ensure Warn When Visiting A Fraudulent Website in Safari Is Enabled (Automated)..371 6.3.4 Ensure Prevent Cross-site Tracking in Safari Is Enabled (Automated).........................373 6.3.5 Audit Hide IP Address in Safari Setting (Manual) ..........................................................376 6.3.6 Ensure Advertising Privacy Protection in Safari Is Enabled (Automated)......................380 6.3.7 Ensure Show Full Website Address in Safari Is Enabled (Automated) .........................382 6.3.8 Audit AutoFill (Manual) ...................................................................................................384 6.3.9 Audit Pop-up Windows (Manual)....................................................................................386 6.3.10 Ensure Show Status Bar Is Enabled (Automated) .......................................................388 

**6.4 Terminal.........................................................................................................................................390** 6.4.1 Ensure Secure Keyboard Entry Terminal.app Is Enabled (Automated) ........................391 **6.5 Passwords.....................................................................................................................................393** 6.5.1 Audit Passwords (Manual) .............................................................................................394 

**7 Supplemental....................................................................................................................... 397 7.1 CIS Apple macOS Benchmark development collaboration with mSCP .................................398 7.2 Apple Push Notification Service (APNs)....................................................................................399 7.3 Mobile Configuration Profiles .....................................................................................................400 7.4 Mobile Device Management (MDM) Software............................................................................401** 

***Appendix: Summary Table.......................................................................................... 403 Appendix: CIS Controls v7 IG 1 Mapped Recommendations................................. 413 Appendix: CIS Controls v7 IG 2 Mapped Recommendations................................. 418 Appendix: CIS Controls v7 IG 3 Mapped Recommendations................................. 423 Appendix: CIS Controls v7 Unmapped Recommendations.................................... 428 Appendix: CIS Controls v8 IG 1 Mapped Recommendations................................. 429 Appendix: CIS Controls v8 IG 2 Mapped Recommendations................................. 434 Appendix: CIS Controls v8 IG 3 Mapped Recommendations................................. 439 Appendix: CIS Controls v8 Unmapped Recommendations.................................... 444 Appendix: Change History .......................................................................................... 445***

Page 6 

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

Page 7 

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

Page 8 

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

Page 9 

Internal Only \- General   
**Target Technology Details** 

This document, CIS Apple macOS 26 Tahoe Benchmark, provides prescriptive  guidance for establishing a secure configuration posture for Apple macOS 26 Tahoe.  This guide was tested against Apple macOS 26 Tahoe. To obtain the latest version of  this guide, please visit https://www.cisecurity.org/cis-benchmarks/. If you have  questions, comments, or have identified ways to improve this guide, please write us at  feedback@cisecurity.org. 

This Benchmark includes instructions for auditing and remediation containing three  different methods: Graphical User Interface (GUI), Command Line Interface using  Terminal (CLI), and Configuration Profiles. These may be used to evaluate current  configuration status and make changes as desired. In most cases, all methods are  

supported by the Operating System and it is up to organizational implementation  personnel on how best to implement. There are some recommendations that can only  be managed through one of these methods. Each organization must decide if control  management outside their standard process is required if no solution is possible through  their organization's specific choice of implementation. It is best practice at this time for  Enterprise-managed devices to use profiles for management. A mix of both profile  device management and command line hardening scripts will be the most  comprehensive solution. 

With the functionality of mobile configuration profiles, there has been an update to  several recommendations. Any recommendation that is user specific but has a profile  that sets a system-wide setting are compliant only with the profile installed. Any user specific settings have been moved to the Additional Information section but will no  longer pass the audit. 

More profile information 

https://developer.apple.com/documentation/devicemanagement 

https://developer.apple.com/documentation/devicemanagement/configuring-multiple devices-using-profiles 

Organizations that are using profiles should remember that a profile can limit what, if  any, settings can be changed based on the profile payload. Even authorized  organization technical personnel may not be able to change a setting with a profile in  place. If technical personnel are expected to make changes that are contrary to profile  settings, the profile may need to be reviewed in order to verify which accounts and what  conditions apply, or a process to temporarily remove the profile should be in place. 

**Intended Audience** 

This document is intended for system and application administrators, security  specialists, auditors, help desk, and platform deployment personnel who plan to  develop, deploy, assess, or secure solutions that incorporate Apple macOS 26 Tahoe.

Page 10 

Internal Only \- General   
**Consensus Guidance** 

This CIS Benchmark™ was created using a consensus review process comprised of a  global community of subject matter experts. The process combines real world  experience with data-based information to create technology specific guidance to assist  users to secure their environments. Consensus participants provide perspective from a  diverse set of backgrounds including consulting, software development, audit and  compliance, security research, operations, government, and legal.  

Each CIS Benchmark undergoes two phases of consensus review. The first phase  occurs during initial Benchmark development. During this phase, subject matter experts  convene to discuss, create, and test working drafts of the Benchmark. This discussion  occurs until consensus has been reached on Benchmark recommendations. The  second phase begins after the Benchmark has been published. During this phase, all  feedback provided by the Internet community is reviewed by the consensus team for  incorporation in the Benchmark. If you are interested in participating in the consensus  process, please visit https://workbench.cisecurity.org/.

Page 11 

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

Page 12 

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

Page 13 

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

Page 14 

Internal Only \- General   
**Profile Definitions**  

The following configuration profiles are defined by this Benchmark: • **Level 1** 

Items in this profile intend to: 

o be practical and prudent; 

o provide a clear security benefit; and 

o not inhibit the utility of the technology beyond acceptable means. • **Level 2** 

This profile extends the "Level 1" profile. Items in this profile exhibit one or more  of the following characteristics: 

o are intended for environments or use cases where security is paramount o acts as defense in depth measure 

o may negatively inhibit the utility or performance of the technology.

Page 15 

Internal Only \- General   
**Acknowledgements** 

This Benchmark exemplifies the great things a community of users, vendors, and  subject matter experts can accomplish through consensus collaboration. The CIS  community thanks the entire consensus team with special recognition to the following  individuals who contributed greatly to the creation of this guide: 

**Author**   
Ron Colvin, Ron Colvin 

**Contributor**   
William Harrison   
Tim Harrison CISSP, ICP, KMP, Center for Internet Security, New York Jason Olsen BSCS, Comerica Bank 

Bob Gendler    
Dan Brodjieski    
Isaac Ordonez , Mann Consulting   
Joe Goerlich , Siemens AG   
Kari Byrd    
John Mahlman    
Matt Durante    
Henry Stamerjohann    
Michael Scarborough    
Allen Golbig    
Mischa van der Bent   
Tony Young    
Andrew Taylor  

**Editor**   
Edward Byrd , Center for Internet Security, New York

Page 16 

Internal Only \- General   
**Recommendations** 

**1 Install Updates, Patches and Additional Security Software** 

Good operational security involves timely remediation of known vulnerabilities. In order  to reduce platform risk, updates need to be deployed in a timely manner. 

CIS recognizes that most organizations require additional third party applications  (security agents, connectivity solutions, productivity applications, etc.) in order to satisfy  various organizational mandates. Such products should be carefully evaluated before  implementation. CIS does not provide specific evaluation and/or compliance criteria for  third party products. If organizations choose to implement third-party solutions, they  should choose solutions that have demonstrated solid commitment to Apple platforms.  Examples of such commitment include but are not limited to: timely support for new  versions of macOS, native code base, and adherence to Apple Developer guidelines  and best practices.

Page 17 

Internal Only \- General   
*1.1 Ensure Apple-provided Software Updates Are Installed  (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

Software vendors release security patches and software updates for their products  when security vulnerabilities are discovered. There is no simple way to complete this  action without a network connection to an Apple software repository. Please ensure  appropriate access for this control. This check is only for what Apple provides through  software update. 

**Rationale:** 

It is important that these updates be applied in a timely manner to prevent unauthorized  persons from exploiting the identified vulnerabilities. 

**Impact:** 

Installation of updates can be disruptive to the users especially if a restart is required.  Major updates need to be applied after creating an organizational patch policy. It is also  advised to run updates and forced restarts during system downtime and not while in  active use.

Page 18 

Internal Only \- General   
**Audit:** 

**Graphical Method:** 

Perform the following to ensure there are no available software updates: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select Show Updates to verify that there are no software updates available 

**Terminal Method:** 

Run the following command to verify there are no software updates currently available: 

| % /usr/bin/sudo /usr/bin/defaults read   /Library/Preferences/com.apple.SoftwareUpdate LastFullSuccessfulDate |
| :---- |

The output will contain the date software update was last checked, ex 2025-09-05  13:28:46 \+0000, and must be within 30 days. 

| % /usr/bin/sudo /usr/bin/defaults read   /Library/Preferences/com.apple.SoftwareUpdate RecommendedUpdates |
| :---- |

The output will show any updates awaiting to be installed, ex: 

| (   {   "Display Name" \= "macOS Tahoe 26.0.1";   "Display Version" \= "26.0.1";   Identifier \= "MSU\_UPDATE\_25A362\_patch\_26.0.1\_minor";  MobileSoftwareUpdate \= 1;   "Product Key" \= "MSU\_UPDATE\_25A362\_patch\_26.0.1\_minor";  }  ) |
| :---- |

**Note:** If you are running a previous version of macOS, the output will say that the  current version is available. As long as the system is on the current point release of  macOS, it is compliant. It is recommended that your organization moves to the current  version of macOS once a .1 version is released. Be aware that old macOS versions will  stop receiving any updates. 

**Note:** Computers that have installed pre-release software in the past will fail this check  if there are pre-release software updates available when audited.

Page 19 

Internal Only \- General   
**Remediation:** 

**Graphical Method:** 

Perform the following to install all available software updates: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select Update All 

**Terminal Method:** 

Run the following command to verify what packages need to be installed: 

| % /usr/bin/sudo /usr/sbin/softwareupdate \-l  |
| :---- |

The output will include the following: Software Update found the following new  or updated software: 

**Note:** If the software update server cannot be reached, that will need further  investigation. This could be due to a network issue and must be resolved within your  organization. 

Run the following command to install all the packages that need to be updated: To install all updates run the command: 

| % /usr/bin/sudo /usr/sbin/softwareupdate \-i \-a |
| :---- |

Or run the following command to install individual packages: 

| % /usr/bin/sudo /usr/sbin/softwareupdate \-i '\<package name\>' |
| :---- |

**Note:** If one of the software updates listed includes Action: restart, then you must  attach the \-R flag to force a system restart. If the system update is complete but no  restart occurs, then the system is in an unknown state that requires a future restart. It is  advised to run updates and forced restarts during system downtime and not while in  active use.

Page 20 

Internal Only \- General   
*example:* 

| % /usr/bin/sudo /usr/sbin/softwareupdate \-l   Software Update Tool  Finding available software  Software Update found the following new or updated software:  \* Label: ProVideoFormats-2.2.7  Title: Pro Video Formats, Version: 2.2.7, Size: 9693KiB, Recommended:  YES,   \* Label: Command Line Tools for Xcode-15.0  Title: Command Line Tools for Xcode, Version: 15.0, Size: 721962KiB,  Recommended: YES,   % /usr/bin/sudo /usr/sbin/softwareupdate \-i 'ProVideoFormats-2.2.7' Software Update Tool  Finding available software  Attempting to quit apps: (   "com.apple.Compressor"  )  Waiting for user to quit any relevant apps  Successfully quit all apps  Downloaded Pro Video Formats  Installing Pro Video Formats  Done with Pro Video Formats  Done. |
| :---- |

In the above example, if a restart was required, the command to remediate would be  /usr/bin/sudo /usr/sbin/softwareupdate \-i 'ProVideoFormats-2.2.7' \-R 

**References:** 

1\. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf

Page 21 

Internal Only \- General   
**Additional Information:** 

If software update has not been ran on the system previously (GUI or in Terminal), then  the End User License agreement may need to be accepted when running  softwareupdate \-i. Where that is needed, include the \--agree-to-license option. 

**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 7.3 Perform Automated Operating System Patch  Management  Perform operating system updates on enterprise assets through automated  patch management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v8 | 7.4 Perform Automated Application Patch Management Perform application updates on enterprise assets through automated patch  management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v7 | 3.4 Deploy Automated Operating System Patch  Management Tools  Deploy automated software update tools in order to ensure that the operating  systems are running the most recent security updates provided by the software  vendor. | ●  | ●  | ● |
| v7 | 3.5 Deploy Automated Software Patch Management  Tools  Deploy automated software update tools in order to ensure that third-party  software on all systems is running the most recent security updates provided by  the software vendor. | ●  | ●  | ● |

Page 22 

Internal Only \- General   
*1.2 Ensure Download New Updates When Available Is Enabled  (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

In the GUI, both "Install macOS updates" and "Install app updates from the App Store"  are dependent on whether "Download new updates when available" is selected. 

**Rationale:** 

It is important that a system has the newest updates downloaded so that they can be  applied. 

**Impact:** 

If "Download new updates when available" is not selected, updates may not be made in  a timely manner and the system will be exposed to additional risk. 

**Audit:** 

Perform the following to ensure the system is automatically checking for updates: **Graphical Method:** 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Verify that Download new updates when available is enabled 

**Terminal Method:** 

Run the following command to verify that software updates are automatically checked: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.SoftwareUpdate')\\ .objectForKey('AutomaticDownload').js  EOS  true |
| :---- |

**Note:** If automatic updates were selected during system setup, this setting may not  have left an auditable artifact. Please turn off the check and re-enable when the GUI  does not reflect the audited results.

Page 23 

Internal Only \- General   
**Remediation:** 

Perform the following to enable the system to automatically check for updates: **Graphical Method:** 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Set Download new updates when available to enabled 

6\. Select Done 

**Terminal Method:** 

Run the following command to enable auto update: 

| % /usr/bin/sudo /usr/bin/defaults write   /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload \-bool true  |
| :---- |

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.SoftwareUpdate 

2\. The key to include is AutomaticDownload 

3\. The key must be set to \<true/\>

Page 24 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 7.3 Perform Automated Operating System Patch  Management  Perform operating system updates on enterprise assets through automated  patch management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v8 | 7.4 Perform Automated Application Patch Management Perform application updates on enterprise assets through automated patch  management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v7 | 3.4 Deploy Automated Operating System Patch  Management Tools  Deploy automated software update tools in order to ensure that the operating  systems are running the most recent security updates provided by the software  vendor. | ●  | ●  | ● |
| v7 | 3.5 Deploy Automated Software Patch Management  Tools  Deploy automated software update tools in order to ensure that third-party  software on all systems is running the most recent security updates provided by  the software vendor. | ●  | ●  | ● |

Page 25 

Internal Only \- General   
*1.3 Ensure Install of macOS Updates Is Enabled (Automated)* **Profile Applicability:**   
• Level 1 

**Description:** 

Ensure that macOS updates are installed after they are available from Apple. This  setting enables macOS updates to be automatically installed. Some environments will  want to approve and test updates before they are delivered. It is best practice to test  first where updates can and have caused disruptions to operations. Automatic updates  should be turned off where changes are tightly controlled and there are mature testing  and approval processes. Automatic updates should not be turned off simply to allow the administrator to contact users in order to verify installation. A dependable, repeatable  process involving a patch agent or remote management tool should be in place before  auto-updates are turned off. 

**Rationale:** 

Patches need to be applied in a timely manner to reduce the risk of vulnerabilities being  exploited. 

**Impact:** 

Unpatched software may be exploited. 

**Audit:** 

**Graphical Method:** 

Perform the following to ensure that macOS updates are set to auto update: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Verify that Install macOS updates is enabled 

**or** 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Automatically Install macOS Updates set  to True

Page 26 

Internal Only \- General   
**Terminal Method:** 

Run the following command to verify that macOS updates are automatically checked  and installed: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.SoftwareUpdate')\\ .objectForKey('AutomaticallyInstallMacOSUpdates').js  EOS  true |
| :---- |

**Note:** If automatic updates were selected during system setup, this setting may not  have left an auditable artifact. Please turn off the check and re-enable when the GUI  does not reflect the audited results. 

**Remediation:** 

**Graphical Method:** 

Perform the following steps to enable macOS updates to run automatically: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Set Install macOS updates to enabled 

6\. Select Done 

**Terminal Method:** 

Run the following command to to enable automatic checking and installing of macOS  updates: 

| % /usr/bin/sudo /usr/bin/defaults write   /Library/Preferences/com.apple.SoftwareUpdate   AutomaticallyInstallMacOSUpdates \-bool TRUE |
| :---- |

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.SoftwareUpdate 

2\. The key to include is AutomaticallyInstallMacOSUpdates 

3\. The key must be set to \<true/\>

Page 27 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 7.3 Perform Automated Operating System Patch  Management  Perform operating system updates on enterprise assets through automated  patch management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v8 | 7.4 Perform Automated Application Patch Management Perform application updates on enterprise assets through automated patch  management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v7 | 3.4 Deploy Automated Operating System Patch  Management Tools  Deploy automated software update tools in order to ensure that the operating  systems are running the most recent security updates provided by the software  vendor. | ●  | ●  | ● |
| v7 | 3.5 Deploy Automated Software Patch Management  Tools  Deploy automated software update tools in order to ensure that third-party  software on all systems is running the most recent security updates provided by  the software vendor. | ●  | ●  | ● |

Page 28 

Internal Only \- General   
*1.4 Ensure Install Application Updates from the App Store Is  Enabled (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

Ensure that application updates are installed after they are available from Apple. These  updates do not require reboots or administrator privileges for end users. 

**Rationale:** 

Patches need to be applied in a timely manner to reduce the risk of vulnerabilities being  exploited. 

**Impact:** 

Unpatched software may be exploited. 

**Audit:** 

**Graphical Method:** 

Perform the following steps to ensure that App Store updates install automatically: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Verify that Install application updates from the App Store is enabled **or** 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Automatically Install App Updates set to  True

Page 29 

Internal Only \- General   
**Terminal Method:** 

Run the following command to verify that App Store updates are auto updating: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  function run() {   let pref1 \=   ObjC.unwrap($.NSUserDefaults.alloc.initWithSuiteName('com.apple.commerce')\\  .objectForKey('AutoUpdate'))   let pref2 \=   ObjC.unwrap($.NSUserDefaults.alloc.initWithSuiteName('com.apple.SoftwareUpdat e')\\   .objectForKey('AutomaticallyInstallAppUpdates'))   if ( pref1 \== 1 || pref2 \== 1 ) {   return("true")   } else {   return("false")   }  }  EOS  true |
| :---- |

**Remediation:** 

**Graphical Method:** 

Perform the following steps to enable App Store updates to install automatically: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Set Install application updates from the App Store to enabled 6\. Select Done 

**Terminal Method:** 

Run the following command to turn on App Store auto updating: 

| % /usr/bin/sudo /usr/bin/defaults write   /Library/Preferences/com.apple.commerce AutoUpdate \-bool TRUE |
| :---- |

**Note:** This remediation requires a log out and log in to show in the GUI. **Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.SoftwareUpdate 

2\. The key to include is AutomaticallyInstallAppUpdates 

3\. The key must be set to \<true/\>

Page 30 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 7.3 Perform Automated Operating System Patch  Management  Perform operating system updates on enterprise assets through automated  patch management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v8 | 7.4 Perform Automated Application Patch Management Perform application updates on enterprise assets through automated patch  management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v7 | 3.4 Deploy Automated Operating System Patch  Management Tools  Deploy automated software update tools in order to ensure that the operating  systems are running the most recent security updates provided by the software  vendor. | ●  | ●  | ● |
| v7 | 3.5 Deploy Automated Software Patch Management  Tools  Deploy automated software update tools in order to ensure that third-party  software on all systems is running the most recent security updates provided by  the software vendor. | ●  | ●  | ● |

Page 31 

Internal Only \- General   
*1.5 Ensure Install Security Responses and System Files Is  Enabled (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

Ensure that system and security updates are installed after they are available from  Apple. This setting enables definition updates for XProtect and Gatekeeper. With this  setting in place, new malware and adware that Apple has added to the list of malware or  untrusted software will not execute. These updates do not require reboots or end user  admin rights. 

Apple has introduced a security feature that allows for smaller downloads and the  installation of security updates when a reboot is not required. This feature is only  available when the last regular update has already been applied. This feature  emphasizes that a Mac must be up-to-date on patches so that Apple's security tools can  be used to quickly patch when a rapid response is necessary. 

**Rationale:** 

Patches need to be applied in a timely manner to reduce the risk of vulnerabilities being  exploited. 

**Impact:** 

Unpatched software may be exploited. 

**Audit:** 

**Graphical Method:** 

Perform the following steps to ensure that system data files and security updates install  automatically: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Verify that Install Security Responses and System files is enabled

Page 32 

Internal Only \- General   
**Terminal Method:** 

Run the following commands to verify that system data files and security updates are  automatically checked: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  function run() {   let pref1 \=   ObjC.unwrap($.NSUserDefaults.alloc.initWithSuiteName('com.apple.SoftwareUpdat e')\\   .objectForKey('ConfigDataInstall'))   let pref2 \=   ObjC.unwrap($.NSUserDefaults.alloc.initWithSuiteName('com.apple.SoftwareUpdat e')\\   .objectForKey('CriticalUpdateInstall'))   if ( pref1 \== 1 && pref2 \== 1 ) {   return("true")   } else {   return("false")   }  }  EOS  true |
| :---- |

**Note:** If automatic updates were selected during system setup, this setting may not  have left an auditable artifact. Please turn off the check and re-enable when the GUI  does not reflect the audited results. 

**Remediation:** 

**Graphical Method:** 

Perform the following steps to enable system data files and security updates to install  automatically: 

1\. Open System Settings 

2\. Select General 

3\. Select Software Update 

4\. Select the i 

5\. Set Install Security Responses and System files to enabled 6\. Select Done

Page 33 

Internal Only \- General   
**Terminal Method:** 

Run the following commands to enable automatic checking of system data files and  security updates: 

| % /usr/bin/sudo /usr/bin/defaults write   /Library/Preferences/com.apple.SoftwareUpdate ConfigDataInstall \-bool true   % /usr/bin/sudo /usr/bin/defaults write   /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall \-bool  true |
| :---- |

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.SoftwareUpdate 

2\. The key to include is ConfigDataInstall 

3\. The key must be set to \<true/\> 

4\. The key to also include is CriticalUpdateInstall 

5\. The key must be set to \<true/\> 

**References:** 

1\. https://eclecticlight.co/2021/10/27/silently-updated-security-data-files-in monterey/ 

2\. https://support.apple.com/en-us/HT202491   
3\. https://support.apple.com/guide/security/protecting-against-malware sec469d47bd8/web 

4\. https://support.apple.com/guide/deployment/rapid-security-responses dep93ff7ea78/1/web/1.0

Page 34 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 7.3 Perform Automated Operating System Patch  Management  Perform operating system updates on enterprise assets through automated  patch management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v8 | 7.4 Perform Automated Application Patch Management Perform application updates on enterprise assets through automated patch  management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v8 | 7.7 Remediate Detected Vulnerabilities  Remediate detected vulnerabilities in software through processes and tooling  on a monthly, or more frequent, basis, based on the remediation process. |  | ●  | ● |
| v7 | 3.4 Deploy Automated Operating System Patch  Management Tools  Deploy automated software update tools in order to ensure that the operating  systems are running the most recent security updates provided by the software  vendor. | ●  | ●  | ● |
| v7 | 3.5 Deploy Automated Software Patch Management  Tools  Deploy automated software update tools in order to ensure that third-party  software on all systems is running the most recent security updates provided by  the software vendor. | ●  | ●  | ● |

Page 35 

Internal Only \- General   
*1.6 Ensure Software Update Deferment Is Less Than or Equal to  30 Days (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

Apple provides the capability to manage software updates on Apple devices through  mobile device management. Part of those capabilities permit organizations to defer  software updates and allow for testing. Many organizations have specialized software  and configurations that may be negatively impacted by Apple updates. If software  updates are deferred, they should not be deferred for more than 30 days. This control  only verifies that deferred software updates are not deferred for more than 30 days. 

**Note:** Software deferment is deprecated by Apple and will be removed in a future OS  release/update. Apple Device Management Profile \- SoftwareUpdate 

**Rationale:** 

Apple software updates almost always include security updates. Attackers evaluate  updates to create exploit code in order to attack unpatched systems. The longer a  system remains unpatched, the greater an exploit possibility exists in which there are  publicly reported vulnerabilities. 

Software updates being deferred are specifically referring to OS updates and not either  major upgrades (ex. upgrading from macOS 15.0 to macOS 26\) or applications from the  App Store. 

**Impact:** 

Some organizations may need more than 30 days to evaluate the impact of software  updates.

Page 36 

Internal Only \- General   
**Audit:** 

Perform the following to ensure that software updates are deferred at most 30 days: **Graphical Method:** 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that Deferred Software Update Delays (Days) is set to ≤ 30 

**Terminal Method:** 

Run the following command to verify that a profile is installed that defers software  updates to at most 30 days: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('enforcedSoftwareUpdateDelay').js  EOS |
| :---- |

If there is an output, it should be ≤ 30\. 

**Note:** If your organization does not use a software deferment mobile configuration,  there will be no output and will pass the audit. 

**Remediation:** 

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is enforcedSoftwareUpdateDelay 

3\. The key must be set to \<integer\>\<1-30\>\</integer\> 

**Note:** The key enforcedSoftwareUpdateDelay is for all updates through software  updates. If your organization needs to delay major OS upgrades on a separate  timescale than minor OS updates (or App Store updates), see the Additional Information  section for a breakdown of what keys to use. 

**References:** 

1\. https://support.apple.com/guide/deployment/about-software-updates depc4c80847a/web

Page 37 

Internal Only \- General   
**Additional Information:** 

The keys to enforce updates by type are as follows: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is enforcedSoftwareUpdateDelay 

3\. The key must be set to \<integer\>\<1-30\>\</integer\> 

4\. The key to include is forceDelayedSoftwareUpdates 

5\. The key must be set to \<true/\> 

**Note:** These 5 items are required to be in the configuration profile no matter what  configuration you are using. 

For minor update delays: 

6\. The key to include is    
enforcedSoftwareUpdateMinorOSDeferredInstallDelay 

7\. The key must be set to \<integer\>\<1-30\>\</integer\> 

For major OS upgrade delays: 

6\. The key to include is    
enforcedSoftwareUpdateMajorOSDeferredInstallDelay 

7\. The key must be set to \<integer\>\<set to your organization's  requirements\>\</integer\> 

8\. The key to include is forceDelayedMajorSoftwareUpdates 

9\. The key must be set to \<true/\> 

**Note:** The major deferment key will still show major upgrades being unavailable unless  the PayloadScope of the mobile configuration profile fire is set to user and not system,  ie. \<string\>User\</string\> 

For App Store update delays: 

10.The key to include is enforcedSoftwareUpdateNonOSDeferredInstallDelay 11.The key must be set to \<integer\>\<1-30\>\</integer\> 

12.The key to include is forceDelayedAppSoftwareUpdates 

13.The key must be set to \<true/\> 

**Note:** For every setting that your organization requires, it must be included in the same  configuration profile. If each key is set it separate profiles it will not function.

Page 38 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 7.3 Perform Automated Operating System Patch  Management  Perform operating system updates on enterprise assets through automated  patch management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v8 | 7.4 Perform Automated Application Patch Management Perform application updates on enterprise assets through automated patch  management on a monthly, or more frequent, basis. | ●  | ●  | ● |
| v7 | 3.4 Deploy Automated Operating System Patch  Management Tools  Deploy automated software update tools in order to ensure that the operating  systems are running the most recent security updates provided by the software  vendor. | ●  | ●  | ● |
| v7 | 3.5 Deploy Automated Software Patch Management  Tools  Deploy automated software update tools in order to ensure that third-party  software on all systems is running the most recent security updates provided by  the software vendor. | ●  | ●  | ● |

Page 39 

Internal Only \- General   
**2 System Settings** 

This section contains recommendations related to configurable options in the System  Settings application. 

At Apple's World Wide Developer Conference (WWDC) 2024, Apple announced Apple  Intelligence as a new feature within both macOS 15 and iOS 18\. As of macOS 15.0.1,  Apple has not released any of the Apple Intelligence capabilities within the operating  system. Those features may be released in future versions based on Apple  announcements of future releases of macOS 15.x. There is ongoing discussion within  the CIS macOS community on what recommendations will be forthcoming. Those  recommendations will be based on released software from Apple. Organizations need  to do their own risk analysis on using Apple's first-party Apple Intelligence features. CIS  will provide further guidance as the first-party functionality is released in future versions  of macOS. The current consensus is around third-party integrations (i.e. ChatGPT). It is  highly recommendation that these integrations are disabled until data loss prevention  and confidential information controls are evaluated.

Page 40 

Internal Only \- General   
**2.1 Apple Account** 

Apple is a hardware manufacturer that develops operating systems for the hardware it  creates. Apple is also a cloud service provider, and those services include applications,  music, books, television, cloud storage, etc. Apple simplifies the process to ensure that  all user devices are entitled to content where the user has purchased access, or is part  of an Apple basic level of entitlement (BLE) for purchasing an Apple device. The use of  an Apple Account allows for a consistent access and experience across all Apple  devices. An Apple Account functions as Single Sign-On access to all Apple-provided  services. It is critical that each user's account is protected appropriately so that  unauthorized access risk is heavily mitigated. 

In rare cases, Apple will send a threat notification to a user where attempts to  compromise an Apple Account have been observed. Apple will NOT send you a link to  sign in to your Apple Account but will direct you to sign in through account.apple.com. 

Managed Apple Accounts are a type of Apple Account managed by organizations and  not owned by individual users. Not all Apple Account services are available to managed  Apple Accounts. Apple keeps a list of available services here: Service access with  Managed Apple Accounts 

• Manage and use your Apple Account   
• If you forgot your Apple Account primary email address or phone number • To find out what devices are signed into an Apple Account, follow these  instructions: Check your Apple Account device list to find where you're signed in • To erase a macOS device and restore it to factory settings, follow these  instructions: Erase your Mac and reset it to factory settings 

• To learn more about Threat Notifications: About Apple threat notifications and  protecting against mercenary spyware and What to do if Apple contacts you  about malware or security 

• Apple Account Wikipedia page   
• What Is an Apple ID/Apple Account? Is it Different from iTunes and iCloud? • Apple Account support page 

• RIP Apple ID: How to Manage Your Apple Account From Anywhere 

**Note:** Previous to WWDC 2024, Apple Accounts were called Apple IDs. There is still a  large amount of media out there that will refer to Apple Accounts as Apple IDs, but the  two are the same service and should not cause any confusion.

Page 41 

Internal Only \- General   
**2.1.1 iCloud** 

iCloud is Apple's service for synchronizing, storing, and backing up data from Apple  applications in both macOS and iOS. 

macOS controls for iCloud are part of the Apple Account settings in macOS. The  configuration options in macOS resemble the options in iOS. 

Apple's iCloud is a consumer-oriented service that allows a user to store data as well as  find, control, and back up devices that are associated with their Apple Account. The use  of iCloud on Enterprise devices should align with the acceptable use policy for devices  that are managed, as well as confidentiality requirements for data handled by the user.  If iCloud is allowed, the data that is copied to Apple servers will likely be duplicated on  both personal as well as Enterprise devices. 

For many users, the Enterprise email system may replace many of the available  features in iCloud. Calendars, notes, and contacts can sync to the official Enterprise  repository and be available through multiple devices if using either an Exchange or  Google environment email. 

Depending on workplace requirements, it may not be appropriate to intermingle  Enterprise and personal bookmarks, photos, and documents. Since the service allows  every device associated with the user's Apple Account to synchronize and have access  to the cloud storage, the concern is not just about having sensitive data on Apple's  servers, but also having that same data on the phone of the teenage son or daughter of  an employee. The use of family sharing options can reduce the risk. 

Apple's iCloud is just one of many cloud-based solutions being used for data  synchronization across multiple platforms, and it should be controlled consistently with  other cloud services in your environment. Work with your employees and configure the  access to best enable data protection for your mission. 

iCloud can also sync a user's photos. If this feature is used where an organization's  proprietary photos are stored, unauthorized access in a commercial cloud will result. 

We are not giving any specific guidance on how your organization should configure  iCloud. To verify, or modify, the iCloud settings you can refer to Apple's support  documents: Change iCloud settings on Mac

Page 42 

Internal Only \- General   
*2.1.1.1 Audit iCloud Passwords & Keychain (Manual)* **Profile Applicability:**   
• Level 2 

**Description:** 

The iCloud Passwords & Keychain is Apple's synchronization service that works with  Apple Accounts to synchronize password, passkey, and credit card information across  macOS, iOS, iPadOS. The capability allows users to use synced password, passkey,  and credit card information in either macOS, iOS, or iPadOS for use in Safari and other  applications. 

The password, passkey, and credit card information stored on macOS in the keychain is  stored in Apple's cloud, including on Enterprise-managed computer. 

When using personal Apple Accounts and credentials may include both enterprise related and personal data, depending on user behavior and account usage patterns. 

**Rationale:** 

Ensure that iCloud Passwords and Keychain usage aligns with organizational  requirements, taking into account whether personal or managed Apple Accounts are  being utilized. 

**Impact:** 

When iCloud Passwords & Keychain is turned off, password, passkey, and credit card  information are no longer synchronized across devices signed in with the same Apple  Account. Passwords, passkeys, and credit card information can still be stored locally  and accessed through the Passwords and Keychain apps, even when iCloud  Passwords & Keychain is turned off.

Page 43 

Internal Only \- General   
**Audit:** 

**Graphical Method:** 

Perform the following steps to verify a profile is installed for the iCloud Passwords &  Keychain sync service: 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Disallow iCloud Keychain Sync set to your  organization's requirements 

**Terminal Method:** 

Run the following command to verify that a profile is installed that sets iCloud  Passwords & Keychain sync to your organization's settings: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('allowCloudKeychainSync').js  EOS |
| :---- |

If the output is false, iCloud Passwords & Keychain Sync is disabled. If the output is  true, iCloud Passwords & Keychain sync is enabled. 

**Remediation:** 

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is allowCloudKeychainSync 

3\. The key should be set \<true/\>, to allow iCloud Passwords & Keychain syncing,  or \<false/\>, to disable it, based on your organization's requirements

Page 44 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v8 | 15.3 Classify Service Providers  Classify service providers. Classification consideration may include one or more  characteristics, such as data sensitivity, data volume, availability requirements,  applicable regulations, inherent risk, and mitigated risk. Update and review  classifications annually, or when significant enterprise changes occur that could  impact this Safeguard. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |
| v7 | 9.2 Ensure Only Approved Ports, Protocols and Services  Are Running  Ensure that only network ports, protocols, and services listening on a system  with validated business needs, are running on each system. |  | ●  | ● |

Page 45 

Internal Only \- General   
*2.1.1.2 Audit iCloud Drive (Manual)* 

**Profile Applicability:** 

• Level 2 

**Description:** 

iCloud Drive is Apple's storage solution for applications on both macOS and iOS to use  the same files that are resident in Apple's cloud storage. The iCloud Drive folder is  available much like Dropbox, Microsoft OneDrive, or Google Drive. 

One of the concerns in public cloud storage is that proprietary data may be  inappropriately stored in an end user's personal repository. Organizations that need  specific controls on information should ensure that this service is turned off or the user  knows what information must be stored on services that are approved for storage of  controlled information. 

**Rationale:** 

Organizations should review third party storage solutions pertaining to existing data  confidentiality and integrity requirements. 

**Impact:** 

Users will not be able to use continuity on macOS to resume the use of newly  composed but unsaved files.

Page 46 

Internal Only \- General   
**Audit:** 

**Graphical Method:** 

Perform the following steps to verify if a profile is installed to configure iCloud Drive: 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Disallow iCloud Drive set to your  organization's requirements 

**Terminal Method:** 

Run the following command to verify that a profile is installed that sets iCloud Drive sync  to your organization's settings: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('allowCloudDocumentSync').js  EOS  |
| :---- |

If the output is false, iCloud Drive Sync is disabled. If the output is true, iCloud Drive  sync is enabled. 

**Remediation:** 

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is allowCloudDocumentSync 

3\. The key should be set \<true/\>, to allow iCloud Drive, or \<false/\>, to disable it,  based on your organization's requirements 

**References:** 

1\. https://developer.apple.com/documentation/devicemanagement/restrictions

Page 47 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v8 | 15.3 Classify Service Providers  Classify service providers. Classification consideration may include one or more  characteristics, such as data sensitivity, data volume, availability requirements,  applicable regulations, inherent risk, and mitigated risk. Update and review  classifications annually, or when significant enterprise changes occur that could  impact this Safeguard. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |

Page 48 

Internal Only \- General   
*2.1.1.3 Ensure iCloud Drive Document and Desktop Sync Is  Disabled (Automated)* 

**Profile Applicability:** 

• Level 2 

**Description:** 

With macOS 10.12, Apple introduced the capability to have a user's Desktop and  Documents folders automatically synchronize to the user's iCloud Drive, provided they  have enough room purchased through Apple on their iCloud Drive. This capability  mirrors what Microsoft is doing with the use of OneDrive and Office 365\. There are  concerns with using this capability. 

The storage space that Apple provides for free is used by users with iCloud mail, all of a  user's Photo Library created with the ever larger Multi-Pixel iPhone cameras, and all  iOS Backups. Adding a synchronization capability for users who have files going back a  decade or more, storage may be tight using the free 5GB provided without purchasing  much larger storage capacity from Apple. Users with multiple computers running 10.12  and above with unique content on each will have issues as well. 

Enterprise users may not be allowed to store Enterprise information in a third-party  public cloud. In previous implementations, such as iCloud Drive or DropBox, the user  selected what files were synchronized even if there were no other controls. The new  feature synchronizes all files in a folder widely used to put working files. 

The automatic synchronization of all files in a user's Desktop and Documents folders  should be disabled. 

https://derflounder.wordpress.com/2016/09/23/icloud-desktop-and-documents-in macos-sierra-the-good-the-bad-and-the-ugly/ 

**Rationale:** 

Automated Document synchronization should be planned and controlled to approved  storage. 

**Impact:** 

Users will not be able to use iCloud for the automatic sync of the Desktop and  Documents folders.

Page 49 

Internal Only \- General   
**Audit:** 

**Graphical Method:** 

Perform the following steps to verify if Desktop and Documents in iCloud Drive is  enabled: 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Disallow iCloud Desktop & Documents  Sync set to True 

**Terminal Method:** 

Run the following command to verify that a profile is installed that disables iCloud  Document and Desktop Sync: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('allowCloudDesktopAndDocuments').js  EOS  false |
| :---- |

**Remediation:** 

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is allowCloudDesktopAndDocuments 

3\. The key must be set to \<false/\> 

**References:** 

1\. https://developer.apple.com/documentation/devicemanagement/restrictions

Page 50 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v8 | 15.3 Classify Service Providers  Classify service providers. Classification consideration may include one or more  characteristics, such as data sensitivity, data volume, availability requirements,  applicable regulations, inherent risk, and mitigated risk. Update and review  classifications annually, or when significant enterprise changes occur that could  impact this Safeguard. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |

Page 51 

Internal Only \- General   
*2.1.1.4 Audit Security Keys Used With Apple Accounts (Manual)* **Profile Applicability:**   
• Level 2 

**Description:** 

Apple has introduced the capability of using security keys to protect Apple Accounts  using two-factor authentication in macOS 13.2, in iOS 16.3, and in iPadOS 16.3. This  feature along with the purchase of two hardware tokens (a backup device is required)  protects against the compromise of Apple Accounts. This feature requires all devices  using an enrolled Apple Account to meet the minimum OS standard. 

**Rationale:** 

Users of Apple devices are supported across their devices by using the same Apple  Account to support shared data in both iCloud and across devices. Compromising an  Apple Account has become a very attractive target for attackers to gain unauthorized  access to iCloud storage and user devices. Two-factor authentication reduces the risk. 

**Impact:** 

Legacy devices and test machines will be challenging to ensure that they are all running  recent Operating Systems that can utilize Security Keys. It is best practice not to use  Apple Accounts with access to current user data on legacy and test machines.  Technical staff that use legacy devices are encouraged to create additional Apple  Accounts that do not need two-factor protection and can be used for testing on legacy  devices when required. 

**Audit:** 

**Graphical Method:** 

Perform the following steps to verify if Security Keys is set to your organization's  requirements: 

1\. Open System Settings 

2\. Select Apple Account 

3\. Select Password & Security 

4\. Verify that Security Keys is set to your organization's requirements

Page 52 

Internal Only \- General   
**Remediation:** 

**Graphical Method:** 

Perform the following steps to set Security Keys is set to your organization's  requirements: 

1\. Open System Settings 

2\. Select Apple Account 

3\. Select Password & Security 

4\. Select Add.. to add a security key, or Remove All Security Keys ro remove  security keys, to meet your organization's requirements 

**References:** 

1\. https://support.apple.com/en-us/102637   
2\. https://9to5mac.com/2023/02/03/ios-16-3-hardware-security-keys-explained video/ 

3\. https://hcsonline.com/images/PDFs/Security\_Key\_Apple\_ID.pdf 

**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| ----- | ----- | ----- | :---: | ----- |
| v8 | 5.2 Use Unique Passwords  Use unique passwords for all enterprise assets. Best practice implementation  includes, at a minimum, an 8-character password for accounts using MFA and a  14-character password for accounts not using MFA.  | ●  | ●  | ● |
| v7 | 4.4 Use Unique Passwords  Where multi-factor authentication is not supported (such as local administrator,  root, or service accounts), accounts will use passwords that are unique to that  system. |  | ●  | ● |

Page 53 

Internal Only \- General   
*2.1.1.5 Audit Freeform Sync to iCloud (Manual)* 

**Profile Applicability:** 

• Level 2 

**Description:** 

Starting with macOS 13.1 Apple has made FreeForm, a collaboration tool, available for  macOS, iOS and iPadOS. This application allows for extensive whiteboard creation and  sharing using iCloud. Organizations may want to audit the use of Freeform iCloud  sharing of internally created boards. 

**Rationale:** 

Internally created whiteboards may not be authorized to share to external contacts  through iCloud. 

**Audit:** 

**Graphical Method:** 

Perform the following steps to verify if iCloud Freeform sync is enabled: 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Disallow iCloud Freeform Sync set to your  organization's requirement 

**Terminal Method:** 

Run the following command to verify that a profile is installed that disables Freeform  Sync: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('allowCloudFreeform').js  EOS |
| :---- |

The output should match your organization's requirement 

**Remediation:** 

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is allowCloudFreeform 

3\. The key must be set to \<\<true/false\>/\>

Page 54 

Internal Only \- General   
**References:** 

1\. https://www.apple.com/newsroom/2022/12/apple-launches-freeform-a-powerful new-app-designed-for-creative-collaboration/ 

2\. https://support.apple.com/guide/freeform/share-a-board-frfma5307056b/mac 3\. https://support.apple.com/guide/icloud/set-up-freeform-mmd1b86048ac/icloud 

**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v8 | 15.3 Classify Service Providers  Classify service providers. Classification consideration may include one or more  characteristics, such as data sensitivity, data volume, availability requirements,  applicable regulations, inherent risk, and mitigated risk. Update and review  classifications annually, or when significant enterprise changes occur that could  impact this Safeguard. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |

Page 55 

Internal Only \- General   
*2.1.1.6 Audit Find My Mac (Manual)* 

**Profile Applicability:** 

• Level 2 

**Description:** 

Find My is Apple's consumer solution for device tracking of your devices. This allows a  user to track the location of devices associated with their Apple Account. This is a great  solution for consumer or user device management and tracking, but it is not meant to be  an enterprise management solution to device tracking and information management on  enterprise managed devices. There are multiple enterprise MDM solutions for managing  organizational devices. 

**Rationale:** 

An enterprise solution should be used for tracking and information management of all  devices, including Apple devices. Apple's Find My solution only handles Apple devices.  If no enterprise solution is available, Find My provides capabilities for a user to manage  and track Apple devices. It is not designed as an enterprise solution, and should not be  used as one. It is better to allow the user to track devices that use their Apple Account  than to have no tracking at all. 

**Impact:** 

There should be no impact on the user while using the device. If someone other than  the user has access to tracking information, this can impact the user and needs to be  researched. Users should audit to ensure that only authorized people have access to  your location. Using multiple solutions for device tracking can unnecessary complexity. 

One of the advantages of Find My... is that personal tracking is under the context of the  user that is signed into their Apple Account on devices and that is secured against  unauthorized access. Blocking this solution in favor of enterprise tools could result in  personal information loss including the collection, and possible misuse, of personal  location information. Organizations should make a risk assessment on device/user  tracking for internal use only.

Page 56 

Internal Only \- General   
**Audit:** 

**Graphical Method:** 

Perform the following steps to verify if Security Keys is set to your organization's  requirements: 

1\. Open System Settings 

2\. Select Apple Account 

3\. Select iCloud 

4\. Select Show More Apps.. 

5\. Verify that Find My Mac is set to your organization's requirements 

**Terminal Method:** 

Run the following command to verify that a profile is installed that disables iCloud  Document and Desktop Sync: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('allowFindMyDevice').js  EOS |
| :---- |

The output will either be true, Find My Device is enabled, or false, Find My Device is  disabled depending on your organizations requirements. 

**Remediation:** 

**Graphical Method:** 

Perform the following steps to set Security Keys is set to your organization's  requirements: 

1\. Open System Settings 

2\. Select Apple Account 

3\. Select iCloud 

4\. Select Show More Apps.. 

5\. Set Find My Mac is set to your organization's requirements

Page 57 

Internal Only \- General   
**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is allowFindMyDevice 

3\. The key must be set to \<\<true/\>or\<false/\>\> depending on your organization's  requirements 

**Note:** Find My Device should only be disabled if your organization is using an enterprise  solution for tracking devices. 

**Note:** This key does not fully disable Find My Device. It removes the Device tab in the  Find My... app. The key allowFindMyFriends can also be used to disable the Friends  tab in the app as well. The DisableFMMiCloudSetting key in the  com.apple.icloud.managed PaylodType can disable the Find My setting, but does not  disable it if it is already enabled. 

**References:** 

1\. https://www.icloud.com/find/   
2\. https://support.apple.com/lt-lt/guide/deployment/depdc4ba8d82/web 3\. https://www.apple.com/legal/privacy/data/en/find-my 

4\. https://support.apple.com/lt-lt/guide/apple-business   
manager/axm812df1dd8/1/web

Page 58 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v8 | 15.3 Classify Service Providers  Classify service providers. Classification consideration may include one or more  characteristics, such as data sensitivity, data volume, availability requirements,  applicable regulations, inherent risk, and mitigated risk. Update and review  classifications annually, or when significant enterprise changes occur that could  impact this Safeguard. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |

Page 59 

Internal Only \- General   
*2.1.2 Audit App Store Password Settings (Manual)* **Profile Applicability:**   
• Level 2 

**Description:** 

With Mac OS X 10.11, Apple added settings for password storage for the App Store in  macOS. These settings parallel the settings in iOS. As with iOS, the choices are a  requirement to provide a password after every purchase or to have a 15-minute grace  period, and whether or not to require a password for free purchases. The response to  this setting is stored in a cookie and processed by iCloud. 

There is plenty of risk information on the wisdom of this setting for parents with children  buying games on iPhones and iPads. The most relevant information here is the  likelihood that users who are not authorized to download software may have physical  access to an unlocked computer where someone who is authorized recently made a  purchase. If that is a concern, a password should be required at all times for App Store  access in the Password Settings controls. 

**Rationale:** 

**Audit:** 

**Graphical Method:** 

Perform the following steps to verify that App Store Passwords are set to your  organization's requirements: 

1\. Open System Settings 

2\. Select Apple Account 

3\. Select Media & Purchases 

4\. Verify that Free Downloads is set to your organization's requirements 5\. Verify that Purchases and In-App Purchases is set to your organization's  requirements 

**Remediation:** 

**Graphical Method:** 

Perform the following steps to set App Store Passwords to your organization's  requirements: 

1\. Open System Settings 

2\. Select Apple Account 

3\. Select Media & Purchases 

4\. Set Free Downloads to your organization's requirements 

5\. Set Purchases and In-App Purchases to your organization's requirements

Page 60 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |

Page 61 

Internal Only \- General   
**2.2 Network** 

The Network System Settings pane includes the firewall settings. macOS has a built in firewall that has two main configuration aspects. Both the Application Layer Firewall  (ALF) and the Packet Filter Firewall (PF) can be used to secure running ports and  services on a Mac. The Application Firewall is the one accessible in System  Preferences under Security. The PF firewall contains many more capabilities than ALF,  but also requires a greater understanding of firewall recipes and rule configurations. For  standard use cases on a Mac, the PF firewall is not necessary. macOS may expose  server services that are reachable remotely, but that is not the primary use case or  design. If custom use cases are required, the PF firewall can provide additional security.  Macs that are used as mobile desktops do not need to use the PF firewall capabilities  unless permanently open ports need to be protected with more granular IP access  controls. 

**Additional information** 

https://www.muo.com/tag/mac-really-need-firewall/ 

https://blog.neilsabol.site/post/quickly-easily-adding-pf-packet-filter-firewall-rules-macos osx/ 

http://marckerr.com/a-simple-guild-to-the-mac-pf-firewall/ 

https://blog.scottlowe.org/2013/05/15/using-pf-on-os-x-mountain-lion/

Page 62 

Internal Only \- General   
*2.2.1 Ensure Firewall Is Enabled (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

A firewall is a piece of software that blocks unwanted incoming connections to a system.  The socketfilter Firewall is what is used when the Firewall is turned on in the Security &  Privacy Preference Pane. Logging is required to appropriately monitor what access is  allowed and denied. The logs can be viewed in the macOS Unified Logs. 

Pprior to macOS 15.0 Sequoia, there were additional step to turn on firewall logging  after enabling the firewall. As of macOS 15, logging is turned on automatically without  user interaction. The logging recommendation has been removed in the macOS 15  benchmark and will not be included going forward. If your organization is looking for  more detailed information about network security, you will need a third-party solution. 

**Rationale:** 

A firewall minimizes the threat of unauthorized users gaining access to your system  while connected to a network or the Internet. 

**Impact:** 

The firewall may block legitimate traffic. Applications that are unsigned will require  special handling. 

**Audit:** 

**Graphical Method:** 

Perform the following steps to ensure the firewall is enabled: 

1\. Open System Settings 

2\. Select Network 

3\. Verify that the Firewall is Active 

**or** 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Firewall set to Enabled

Page 63 

Internal Only \- General   
**Terminal Method:** 

Run the following command to verify that the firewall is enabled: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.security.firewall')\\ .objectForKey('EnableFirewall').js  EOS  true |
| :---- |

Also, the status of the firewall can be checked with the binary. Run the following  command to verify if the firewall is enabled with the binary: 

| % /usr/bin/sudo /usr/libexec/ApplicationFirewall/socketfilterfw \-- getglobalstate |
| :---- |

The output will either be Firewall is enabled. (State \= 1\) or Firewall is  enabled. (State \= 2\) if the firewall is enabled. If the firewall is disabled, the output  will be Firewall is disabled. (State \= 0\) 

**Remediation:** 

**Graphical Method:** 

Perform the following steps to turn the firewall on: 

1\. Open System Settings 

2\. Select Network 

3\. Select Firewall 

4\. Set Firewall to enabled 

**Terminal Method:** 

Run the following command to enable the firewall: 

| % /usr/bin/sudo /usr/libexec/ApplicationFirewall/socketfilterfw \-- setglobalstate on  |
| :---- |

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.security.firewall 

2\. The key to include is EnableFirewall 

3\. The key must be set to \<true/\> 

**References:** 

1\. https://support.apple.com/guide/security/firewall-security-in-macos seca0e83763f/web 

2\. https://support.apple.com/guide/mac-help/block-connections-to-your-mac-with-a firewall-mh34041/mac

Page 64 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | ----- | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.5 Implement and Manage a Firewall on End-User  Devices  Implement and manage a host-based firewall or port-filtering tool on end-user  devices, with a default-deny rule that drops all traffic except those services and  ports that are explicitly allowed. | ●  | ●  | ● |
| v8 | 13.1 Centralize Security Event Alerting  Centralize security event alerting across enterprise assets for log correlation and  analysis. Best practice implementation requires the use of a SIEM, which includes  vendor-defined event correlation alerts. A log analytics platform configured with  security-relevant correlation alerts also satisfies this Safeguard. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |
| v7 | 9.4 Apply Host-based Firewalls or Port Filtering Apply host-based firewalls or port filtering tools on end systems, with a default deny rule that drops all traffic except those services and ports that are explicitly  allowed. | ●  | ●  | ● |
| v7 | 9.5 Implement Application Firewalls  Place application firewalls in front of any critical servers to verify and validate the  traffic going to the server. Any unauthorized traffic should be blocked and logged. |  |  | ● |

Page 65 

Internal Only \- General   
*2.2.2 Ensure Firewall Stealth Mode Is Enabled (Automated)* **Profile Applicability:**   
• Level 1 

**Description:** 

While in Stealth mode, the computer will not respond to unsolicited probes, dropping  that traffic. 

**Rationale:** 

Stealth mode on the firewall minimizes the threat of system discovery tools while  connected to a network or the Internet. 

**Impact:** 

Traditional network discovery tools like ping will not succeed. Other network tools that  measure activity and approved applications will work as expected. 

This control aligns with the primary macOS use case of a laptop that is often connected  to untrusted networks where host segregation may be non-existent. In that use case,  hiding from the other inmates is likely more than desirable. In use cases where use is  only on trusted LANs with static IP addresses, stealth mode may not be desirable. 

**Audit:** 

**Graphical Method:** 

Perform the following steps to verify the firewall has stealth mode enabled: 

1\. Open System Settings 

2\. Select Network 

3\. Select Firewall 

4\. Select Option 

5\. Verify that Enable stealth mode is enabled 

**or** 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Stealth Mode set to Enabled

Page 66 

Internal Only \- General   
**Terminal Method:** 

Run the following command to verify that stealth mode is enabled: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.security.firewall')\\ .objectForKey('EnableStealthMode').js  EOS  true |
| :---- |

Also, the status of the stealth mode can be checked with the binary. Run the following  command to verify if the firewall is enabled with the binary: 

| % /usr/libexec/ApplicationFirewall/socketfilterfw \--getstealthmode Firewall stealth mode is on |
| :---- |

**Remediation:** 

**Graphical Method:** 

Perform the following steps to enable firewall stealth mode: 

1\. Open System Settings 

2\. Select Network 

3\. Select Firewall 

4\. Select Options... 

5\. Set Enabled stealth mode to enabled 

**Terminal Method:** 

Run the following command to enable stealth mode: 

| % /usr/bin/sudo /usr/libexec/ApplicationFirewall/socketfilterfw \-- setstealthmode on  Stealth mode enabled |
| :---- |

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.security.firewall 

2\. The key to include is EnableStealthMode 

3\. The key must be set to \<true/\> 

**Note:** This key must be set in the same configuration profile with EnableFirewall set  to \<true/\>. If it is set in its own configuration profile, it will fail. 

**References:** 

1\. http://support.apple.com/en-us/HT201642

Page 67 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.5 Implement and Manage a Firewall on End-User  Devices  Implement and manage a host-based firewall or port-filtering tool on end-user  devices, with a default-deny rule that drops all traffic except those services and  ports that are explicitly allowed. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |
| v7 | 9.4 Apply Host-based Firewalls or Port Filtering Apply host-based firewalls or port filtering tools on end systems, with a default deny rule that drops all traffic except those services and ports that are explicitly  allowed. | ●  | ●  | ● |

Page 68 

Internal Only \- General   
**2.3 General**

Page 69 

Internal Only \- General   
**2.3.1 AirDrop & Handoff**

Page 70 

Internal Only \- General   
*2.3.1.1 Ensure AirDrop Is Disabled When Not Actively  Transferring Files (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

AirDrop is Apple's built-in, on-demand, ad hoc file exchange system that is compatible  with both macOS and iOS. It uses Bluetooth LE for discovery that limits connectivity to  Mac or iOS users that are in close proximity. Depending on the setting, it allows  everyone or only Contacts to share files when they are near each other. 

In many ways, this technology is far superior to the alternatives. The file transfer is done  over a TLS encrypted session, does not require any open ports that are required for file  sharing, does not leave file copies on email servers or within cloud storage, and allows  for the service to be mitigated so that only people already trusted and added to contacts  can interact with you. 

While there are positives to AirDrop, there are privacy concerns that could expose  personal information. For that reason, AirDrop should be disabled, and should only be  enabled when needed and disabled afterwards. The recommendation against enabling  the sharing is not based on any known lack of security in the protocol, but for specific  user operational concerns. 

• If AirDrop is enabled, the Mac is advertising that a Mac is addressable on the  local network and open to either unwanted AirDrop upload requests or for a  negotiation on whether the remote user is in the user's contacts list. Neither  process is desirable. 

• In most known use cases, AirDrop use qualifies as ad hoc networking when it  involves Apple device users deciding to exchange a file using the service.  AirDrop can thus be enabled on the fly for that exchange. 

For organizations concerned about any use of AirDrop because of Digital Loss  Prevention (DLP) monitoring on other protocols, Jamf has an article on reviewing  AirDrop logs. 

Detecting outbound AirDrop transfers and logging them 

**Rationale:** 

AirDrop can allow malicious files to be downloaded from unknown sources. Contacts  Only limits may expose personal information to devices in the same area. 

**Impact:** 

Disabling AirDrop can limit the ability to move files quickly over the network without  using file shares.

Page 71 

Internal Only \- General   
**Audit:** 

**Graphical Method:** 

Perform the following steps to ensure that AirDrop is disabled: 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Allow AirDrop set to False 

**Terminal Method:** 

Run the following command to verify that a profile is installed that disabled AirDrop: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('allowAirDrop').js  EOS  false |
| :---- |

**Remediation:** 

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is allowAirDrop 

3\. The key must be set to \<false/\> 

**Note:** AirDrop can only be enabled or disabled through configuration profiles. If your  organization wants to use AirDrop, it would need to be set through Terminal or the GUI. 

**References:** 

1\. https://www.techrepublic.com/article/apple-airdrop-users-reportedly-vulnerable to-security-flaw/ 

2\. https://www.imore.com/how-apple-keeps-your-airdrop-files-private-and-secure 3\. https://en.wikipedia.org/wiki/AirDrop 

4\. https://macmost.com/10-reasons-you-should-be-using-airdrop-to-transfer files.html 

**Additional Information:** 

To configure AirDrop with more granularity than the profile allows, your organization  should look into third-party applications. An example is Air Drop Assistant.

Page 72 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | ----- | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v8 | 6.7 Centralize Access Control  Centralize access control for all enterprise assets through a directory service or  SSO provider, where supported. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |
| v7 | 15.4 Disable Wireless Access on Devices if Not Required Disable wireless access on devices that do not have a business purpose for  wireless access. |  |  | ● |

Page 73 

Internal Only \- General   
*2.3.1.2 Ensure AirPlay Receiver Is Disabled (Automated)* **Profile Applicability:**   
• Level 1 

**Description:** 

In macOS Monterey (12.0), Apple has added the capability to share content from  another Apple device to the screen of a host Mac. While there are many valuable uses  of this capability, such sharing on a standard Mac user workstation should be enabled  ad hoc as required rather than allowing a continuous sharing service. The feature can  be restricted by Apple Account or network and is configured to use by accepting the  connection on the Mac. Part of the concern is frequent connection requests may  function as a denial-of-service and access control limits may provide too much  information to an attacker. 

https://macmost.com/how-to-use-a-mac-as-an-airplay-receiver.html https://support.apple.com/guide/mac-pro-rack/use-airplay-apdf1417128d/mac **Rationale:** 

This capability appears very useful for kiosk and shared work spaces. The ability to  allow by network could be especially useful on segregated guest networks where  visitors could share their screens on computers with bigger monitors, including  computers connected to projectors. 

**Impact:** 

Turning off AirPlay sharing by default will not allow users to share without turning the  service on. The service should be enabled as needed rather than left on. 

**Audit:** 

**Graphical Method:** 

Perform the following steps to ensure that AirPlay Receiver is Disabled: 

1\. Open System Settings 

2\. Select General 

3\. Select Device Management 

4\. Verify that an installed profile has Allow AirPlay Incoming Requests set to  False

Page 74 

Internal Only \- General   
**Terminal Method:** 

For each user, run the following command to verify that AirPlay Receiver is disabled: 

Run the following command to verify that a profile is installed that disables the ability to  use the computer as an AirPlay Receiver: 

| % /usr/bin/sudo /usr/bin/osascript \-l JavaScript \<\< EOS  $.NSUserDefaults.alloc.initWithSuiteName('com.apple.applicationaccess')\\ .objectForKey('allowAirPlayIncomingRequests').js  EOS  false |
| :---- |

**Remediation:** 

**Profile Method:** 

Create or edit a configuration profile with the following information: 

1\. The PayloadType string is com.apple.applicationaccess 

2\. The key to include is allowAirPlayIncomingRequests 

3\. The key must be set to \<false/\> 

**Default Value:** 

AirPlay Receiver is enabled by default.

Page 75 

Internal Only \- General   
**CIS Controls:**

| Controls  Version  | Control  |  | IG 1 IG 2 IG 3 |  |
| :---: | ----- | ----- | :---: | ----- |
| v8 | 4.1 Establish and Maintain a Secure Configuration Process Establish and maintain a secure configuration process for enterprise assets  (end-user devices, including portable and mobile, non-computing/IoT devices, and   servers) and software (operating systems and applications). Review and update  documentation annually, or when significant enterprise changes occur that could  impact this Safeguard. | ●  | ●  | ● |
| v8 | 4.8 Uninstall or Disable Unnecessary Services on  Enterprise Assets and Software  Uninstall or disable unnecessary services on enterprise assets and software,  such as an unused file sharing service, web application module, or service function. |  | ●  | ● |
| v7 | 5.1 Establish Secure Configurations  Maintain documented, standard security configuration standards for all  authorized operating systems and software. | ●  | ●  | ● |
| v7 | 9.2 Ensure Only Approved Ports, Protocols and Services  Are Running  Ensure that only network ports, protocols, and services listening on a system  with validated business needs, are running on each system. |  | ●  | ● |

Page 76 

Internal Only \- General   
**2.3.2 Date & Time** 

This section contains recommendations related to the configurable items under the  Date & Time panel.

Page 77 

Internal Only \- General   
*2.3.2.1 Ensure Set Time and Date Automatically Is Enabled  (Automated)* 

**Profile Applicability:** 

• Level 1 

**Description:** 

Correct date and time settings are required for authentication protocols, file creation,  modification dates, and log entries. 

**Note:** If your organization has internal time servers, enter them here. Enterprise mobile  devices may need to use a mix of internal and external time servers. If multiple servers  are required, use the Date & Time System Preference with each server separated by a space. 

**Additional Note:** The default Apple time server is time.apple.com. Variations include  time.euro.apple.com. While it is certainly more efficient to use internal time servers,  there is no reason to block access to global Apple time servers or to add a  time.apple.com alias to internal DNS records. There are no reports that Apple gathers  any information from NTP synchronization, as the computers already phone home to  Apple for Apple services including iCloud use and software updates. Best practice is to  allow DNS resolution to an authoritative time service for time.apple.com, preferably to  connect to Apple servers, but local servers are acceptable as well. 

**Rationale:** 

Kerberos may not operate correctly if the time on the Mac is off by more than 5 minutes.  This in turn can affect Apple's single sign-on feature, Active Directory logons, and other  features. 

**Impact:** 

The timed service will periodically synchronize with named time servers and will make  the computer time more accurate.

Page 78 

Internal Only \- General   
**Audit:** 

**Graphical Method:** 

Perform the following steps to ensure that the system's date and time are set  automatically: 

1\. Open System Settings 

2\. Select General 

3\. Select Date & Time 

4\. Verify that Set time and date automatically is enabled 

**Terminal Method:** 

Run the following command to ensure that date and time are automatically set: 

| % /usr/bin/sudo /usr/sbin/systemsetup \-getusingnetworktime   Network Time: On |
| :---- |

**Remediation:** 

**Graphical Method:** 

Perform the following to enable the date and time to be set automatically: 

1\. Open System Settings 

2\. Select General 

3\. Select Date & Time 

4\. Set Set time and date automatically to enabled 

**Note:** By default, the operating system will use time.apple.com as the time server.  You can change to any time server that meets your organization's requirements.

Page 79 

Internal Only \- General 