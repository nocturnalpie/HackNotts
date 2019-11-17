import { Component, OnInit } from '@angular/core';

const SMALL_WIDTH_BREAKPOINT = 720;
@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss']
})
export class SidenavComponent implements OnInit {

  private mediamatcher: MediaQueryList = matchMedia(`(max-width: ${SMALL_WIDTH_BREAKPOINT}px)`);

  constructor() {}

  ngOnInit() {
  }

  isScreenSmall(): boolean {
    return this.mediamatcher.matches;
  }
}
