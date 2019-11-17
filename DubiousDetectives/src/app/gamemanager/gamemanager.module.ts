import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MaterialModule } from '../shared/material.module';
import { FormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';

import { GamemanagerAppComponent } from './gamemanager-app.component';
import { ToolbarComponent } from './components/toolbar/toolbar.component';
import { MainContentComponent } from './components/main-content/main-content.component';
import { SidenavComponent } from './components/sidenav/sidenav.component';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  {path: '', component: GamemanagerAppComponent,
    children: [
      { path: '', component: MainContentComponent }
    ]},
  {path: '**', redirectTo: ''}
];

@NgModule({
  declarations: [GamemanagerAppComponent, ToolbarComponent, MainContentComponent, SidenavComponent],
  imports: [
    CommonModule,
    MaterialModule,
    FormsModule,
    FlexLayoutModule,
    RouterModule.forChild(routes)
  ]
})
export class GamemanagerModule { }
