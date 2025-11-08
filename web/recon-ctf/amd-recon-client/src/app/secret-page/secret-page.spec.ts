import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SecretPage } from './secret-page';

describe('SecretPage', () => {
  let component: SecretPage;
  let fixture: ComponentFixture<SecretPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SecretPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SecretPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
