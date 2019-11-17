import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  {path: 'gamemanager', loadChildren: './gamemanager/gamemanager.module#GamemanagerModule'},
  {path: 'game', loadChildren: './game/game.module#GameModule'},
  {path: '**', redirectTo: 'gamemanager'}
];

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    RouterModule.forRoot(routes),
    BrowserModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
