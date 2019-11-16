import { DubiousDetectivesPage } from './app.po';

describe('dubious-detectives App', function() {
  let page: DubiousDetectivesPage;

  beforeEach(() => {
    page = new DubiousDetectivesPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
