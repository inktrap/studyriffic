# Developer Guide

If you really want to develop Studyriffic, please get [in touch](https://inktrap.org).

## Future Development

Studyriffic fulfills it's purpose. Nevertheless there is always room for improvement. Short term goals are

 - Studyriffic does not work with IE or Edge. I spent one or two days on this problem. [Obviously](https://bugs.launchpad.net/ubuntu/+bug/1) Microsoft [Windows has it's place](https://blog.inktrap.org/windows.html) but I concluded that supporting IE was not worth the effort and simply not a priority. However, if you want to solve a mystery ([and think this is okay](https://www.fefe.de/nowindows/)), be my guest.
 - restructure the tasks_module and separate it into smaller modules, e.g. into restrictions and selection logic, where the logic for selections could be separated further by method (e.g. random, predefined, …)
 - restructure the corresponding tests and clean them up
 - is bottle's cookie function vulnerable to CSRF and should the endpoints look
 out for tokens?

**Long term goals** would include

 - to separate the study/frontend from the backend, like it is done by [experigen](https://github.com/aquincum/experigen).
 - It would also be nice to support more types of tasks and their arbitrary combination, which could be achieved by a modular task creation and processing logic.
 - This could, in addition to being a self-hosted open-source project, be offered as a service. Voilà, there is your startup.

